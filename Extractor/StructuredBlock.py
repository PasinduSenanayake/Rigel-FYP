from Block import Block
from Directive import Directive
from ForLoop import ForLoop
import re

class StructuredBlock(Block):
    def __init__(self, directive, associatedLoop, forLoops, sourceCode):
        elements = []
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

    def vectorize(self, vectorLen=None, alignment=None):
        if not self.directive():
            self.elements.insert(0, Block("pragma\n", 0))



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
                return True
        else:
            if isinstance(self.elements[0], ForLoop):
                return True
        return False


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
        return {"blockStartIndex":blockStartIndex - 1, "blockEndIndex":startIndex+blockLength}

    # def scheduleStatic(self):
    #     if isinstance(self.elements[0], Directive):
    #         self.elements[0].setSchedule("static")
    #     for element in self.elements:
    #         if isinstance(element, StructuredBlock):
    #             element.scheduleStatic()

