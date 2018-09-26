from Block import Block
from Directive import Directive
from Clause import Clause
from ForLoop import ForLoop
from Parameter import Parameter
import re
import copy


class StructuredBlock(Block):
    def __init__(self, directive, associatedLoop, forLoops, sourceCode):
        elements = []
        self.vectorized = False
        if(directive):
            elements.append(directive)
            super(StructuredBlock, self).__init__("", directive.getStartIndex())
            if(not associatedLoop):
                directiveEndIndex = directive.startIndex + directive.length()
                if(directive.details["general"]["type"] == "BasicStructured"):
                    blockDetails = self.getBlockLength(sourceCode, directiveEndIndex)
                    elements.append(Block(sourceCode[blockDetails["blockStartIndex"]:blockDetails["blockEndIndex"]], blockDetails["blockStartIndex"]))
                elif (directive.details["general"]["type"] == "ForStructured"):
                    loopDistance = float("inf")
                    closestLoop = None
                    for loop in forLoops:
                        distance = loop.startIndex - directive.startIndex
                        if distance >= 0 and loopDistance > distance:
                            loopDistance = distance
                            closestLoop = loop
                    elements.append(closestLoop)
            else:
                elements.append(associatedLoop)
        elif associatedLoop:
            elements.append(associatedLoop)
            super(StructuredBlock, self).__init__("", associatedLoop.getStartIndex())
        super(StructuredBlock, self).setElements(elements)

    def directive(self):
        if(isinstance(self.elements[0], Directive)):
            return self.elements[0]
        return None

    def vectorize(self, vectorLen=None, alignment=None, collapsed=None):
        if not self.directive():
            if not collapsed:
                newPragma = Block("\n#pragma omp simd simdlen(" + str(vectorLen) + ")\n", 0)
                # newPragma = Block("#pragma omp simd simdlen(8)\n", 0)
                self.vectorized = True
                newPragma.parent = self
                self.elements.insert(0, newPragma)
            if (collapsed and self.lineNumber < int(collapsed)):
                iterator = self.hasAssociatedLoop()
                collapseSize = 0
                while iterator.lineNumber != int(collapsed):
                    if isinstance(iterator, ForLoop):
                        collapseSize += 1
                    iterator = iterator.getNext()
                collapseSize += 1
                newPragma = Block("\n#pragma omp simd simdlen(" + str(vectorLen) +
                                  ") collapse(" + str(collapseSize) + ")\n", 0)
                # newPragma = Block("#pragma omp simd simdlen(8)\n", 0)
                self.vectorized = True
                newPragma.parent = self
                self.elements.insert(0, newPragma)
            elif collapsed and self.lineNumber > int(collapsed):
                iterator = self.hasAssociatedLoop()
                collapseSize = 1
                while iterator.lineNumber != int(collapsed):
                    iterator = iterator.getParentLoop()
                    collapseSize += 1
                newPragma = Block("\n#pragma omp simd simdlen(" + str(vectorLen) +
                                  ") collapse(" + str(collapseSize) + ")\n", 0)
                # newPragma = Block("#pragma omp simd simdlen(8)\n", 0)
                structuredBlock = iterator.getParent()
                structuredBlock.vectorized = True
                newPragma.parent = structuredBlock
                structuredBlock.elements.insert(0, newPragma)




    def offload(self, pragma=None, num_threads=1, clauses=""):
        if not self.directive():
            threadClause = Clause(name="num_threads", directiveDetails=Directive.directivesDict[pragma]["clauses"], haveParameters=True, elements=[Parameter(0, num_threads, [])])
            threadClause.outerSpacing = ") "
            threadClause.innerSpacing = "("
            newPragma = Directive(self.startIndex, name=pragma, elements=[threadClause,Block(clauses,self.startIndex)])
            newPragma.outerSpacing = "\n"
            newPragma.innerSpacing = " "
            # newPragma = Block("#pragma omp simd simdlen(8)\n", 0)
            newPragma.parent = self
            self.elements.insert(0, newPragma)
            return newPragma


    # def isChild(self, parent):
    #     if parent.getStartIndex() < self.getStartIndex() and self.getStartIndex() < parent.getEndIndex():
    #         return True
    #     return False

    def addChild(self, child):
        for i, item in enumerate(self.elements):
            if child.isChildByIndex(item):
                if isinstance(item, StructuredBlock) or isinstance(item, ForLoop):
                    item.addChild(child)
                else:
                    a = child.getStartIndex() - item.getStartIndex()
                    b = child.getEndIndex() - item.getStartIndex()
                    block1 = Block(item.body[:a], item.getStartIndex())
                    block2 = child
                    block3 = Block(item.body[b+1:], child.getEndIndex()+1)
                    del self.elements[i]
                    self.addElement(i, block3)
                    self.addElement(i, block2)
                    self.addElement(i, block1)
                break

    def hasAssociatedLoop(self):
        if self.directive():
            if isinstance(self.elements[1], ForLoop):
                return self.elements[1]
        else:
            if isinstance(self.elements[0], ForLoop):
                return self.elements[0]
        return None



    def getBlockLength(self, string, startIndex):
        openedBracketCount = 0
        blockLength = 0
        blockStartIndex = 0
        for char in string[startIndex:]:
            blockLength += 1
            if (char == "{"):
                if (openedBracketCount == 0):
                    blockStartIndex = startIndex + blockLength
                openedBracketCount += 1
            if (char == "}"):
                openedBracketCount = openedBracketCount - 1
                if (openedBracketCount == 0):
                    break
        return {"blockStartIndex":blockStartIndex-1, "blockEndIndex":startIndex+blockLength}

    def distribute(self, section, chunk):
        mainBlocks = []
        mainSection = []
        subSection = []
        forLoop = self.hasAssociatedLoop()
        nextObj = forLoop.getNext()
        while nextObj and nextObj.isChild(forLoop):
            if str(nextObj.lineNumber) in section:
                mainBlocks.append(nextObj)
            nextObj = nextObj.getNext()

        nextObj = forLoop.getNext()
        while nextObj and nextObj.isChild(forLoop):
            found = False
            for i in range(len(mainBlocks)):
                if mainBlocks[i].isChild(nextObj) or mainBlocks[i] == nextObj:
                    mainSection.append(nextObj)
                    found = True
                    break
            if not found:
                subSection.append(nextObj)
            nextObj = nextObj.getParallelNext()

        distributed = True
        for section in subSection:
            if ";" in section.body or isinstance(section, StructuredBlock):
                distributed = False

        if not distributed and len(mainSection)>0:
            forLoop.setElements(mainSection)
            newForLoop = copy.deepcopy(forLoop)
            forLoop.innerSpacing = "{\n"
            forLoop.outerSpacing = "\n}\n"
            newForLoop.setElements(subSection, sort=False)
            newStructuredBlock = StructuredBlock(None, newForLoop, None, None)
            newStructuredBlock.startIndex = newForLoop.startIndex
            newStructuredBlock.parent = self.parent
            if forLoop.distributedIndex == int(chunk):
                forLoop.distributed = True
                newForLoop.distributedIndex += 1
                self.parent.elements.insert(self.parent.elements.index(self) + 1, newStructuredBlock)
            else:
                newForLoop.distributed = True
                newForLoop.distributedIndex = forLoop.distributedIndex
                forLoop.distributedIndex = newForLoop.distributedIndex+1
                self.parent.elements.insert(self.parent.elements.index(self), newStructuredBlock)

        # delimiter = Block("\n}\n" + self.body + "{\n")
        # delimiter.parent = self
        # self.elements = mainSection + [delimiter] + subSection

    # def scheduleStatic(self):
    #     if isinstance(self.elements[0], Directive):
    #         self.elements[0].setSchedule("static")
    #     for element in self.elements:
    #         if isinstance(element, StructuredBlock):
    #             element.scheduleStatic()

