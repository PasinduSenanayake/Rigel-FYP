import re
from ForLoop import ForLoop
from Directive import Directive
from StructuredBlock import StructuredBlock
from Block import Block
from pprint import pprint
import copy

class SourceCode:
    def __init__(self, code):
        self.code = code
        self.forLoops = []
        self.directives = []
        self.structure = []
        # self.removeBlockComments()
        # self.removeLineComments()
        self.searchForLoops()
        self.searchDirectives()
        self.root = self.structureCode()
        self.root.setLineNumber(1)
        self.serialroot = self.getSerialCode(self.root)
        self.serialparalleMapping = self.serialParallelMap()

    def isBlockComments(self, index):
        tempSource = self.code
        regex = re.compile(r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)",
                           re.DOTALL)  # error if block comment syntax found in a string construct or in a line comment
        matching = regex.search(tempSource)
        while (matching):
            if matching.start() <= index <= matching.end():
                return True
            tempSource = tempSource[:matching.start()] + tempSource[matching.end():]
            matching = regex.search(tempSource)

    def isLineComments(self, index):
        tempSource = self.code
        regex = re.compile(r"(//.*)", re.DOTALL)  # error if line comment syntax found in a string construct or in a block comment
        matching = regex.search(tempSource)
        while (matching):
            commentLength = 0
            for char in tempSource[matching.start():]:
                commentLength += 1
                if char == "\n":
                    break
            if matching.start() <= index <= matching.start() + commentLength - 1:
                return True
            tempSource = tempSource[:matching.start()] + tempSource[matching.start() + commentLength - 1:]
            matching = regex.search(tempSource)

    def searchForLoops(self):
        sourceCode = self.code
        regex = re.compile(r"for[^\S]*\(", re.DOTALL)  # playfor() method will be caught too
        matching = regex.search(sourceCode)
        while (matching and not self.isBlockComments(matching.start()) and not self.isLineComments(matching.start())):
            loop = ForLoop(matching.start(),sourceCode)
            self.forLoops.append(loop)
            sourceCode = sourceCode[:matching.start()] + "@" * 3 + sourceCode[matching.start() + 3:]
            matching = regex.search(sourceCode)

    def searchDirectives(self):      # assumed "\" is not within pragma directive
        sourceCode = self.code
        regex = re.compile(r"#[^\S]*pragma[^\S]*omp", re.DOTALL)
        matching = regex.search(sourceCode)
        while (matching and not self.isBlockComments(matching.start()) and not self.isLineComments(matching.start())):
            directive = Directive(matching.start(), sourceCode)
            self.directives.append(directive)
            sourceCode = sourceCode[:matching.start()] + "@@@" + sourceCode[matching.start() + 3:]
            matching = regex.search(sourceCode)

    def structureCode(self):
        unstructuredForLoops = self.forLoops[:]
        structure = []
        for directive in self.directives:
            structure.append(StructuredBlock(directive, None, self.forLoops, self.code))
        for structuredBlock in structure:
            if structuredBlock.elements[1] in unstructuredForLoops:
                unstructuredForLoops.remove(structuredBlock.elements[1])
        for loop in unstructuredForLoops:
            structure.append(StructuredBlock(None, loop, self.forLoops, self.code))

        structure.sort(key=lambda x: x.getStartIndex(), reverse=False)

        for structuredBlock in structure:
            structuredBlock.fillSpaces(self.code)

        structure.sort(key=lambda x: x.length(), reverse=False)
        for structuredBlockItr in range(len(structure)):
            for innerItr in range(structuredBlockItr+1,len(structure)):
                if structure[structuredBlockItr].isChildByIndex(structure[innerItr]):
                    structure[innerItr].addChild(structure[structuredBlockItr])

        out = []
        structure.sort(key=lambda x: x.length(), reverse=True)
        for i in structure:
            child = False
            for j in out:
                if i.isChildByIndex(j):
                    child = True
            if not child:
                out.append(i)

        out.sort(key=lambda x: x.getStartIndex(), reverse=False)
        rem = []
        start = 0
        for i in out:
            dif = i.getStartIndex() - start
            if (dif > 0):
                rem.append(Block(self.code[start: i.getStartIndex()], start))
            start = i.getEndIndex() + 1
        rem.append(Block(self.code[start:], start))

        out = out + rem
        out.sort(key=lambda x: x.getStartIndex(), reverse=False)
        rootBlock =  Block("", 0)
        rootBlock.setElements(out)
        return rootBlock

    def setSchedule(self, lineNumber, mechanism):
        self.root.setSchedule(lineNumber, mechanism)

    def getCotent(self):
        return self.root.getContent()

    def writeToFile(self, file, root):
        file = open(file, "w")
        file.write(root.getContent())
        file.close()

    def getSerialCode(self, root):
        serialRoot = copy.deepcopy(self.root)
        nextObj = serialRoot
        while nextObj:
            if isinstance(nextObj, StructuredBlock):
                if nextObj.directive():
                    nextObj.directive().remove()
                    if not nextObj.hasAssociatedLoop():
                        nextObj.elements[1].body = nextObj.elements[1].body[1:]
                        nextObj.elements[-1].body = nextObj.elements[-1].body[:-1]
                    # if not isinstance(nextObj.elements[1], ForLoop):
                    #     print nextObj.elements[1].body[0]
                    #     print "---"
            nextObj = nextObj.getNext()
        serialRoot.setLineNumber(1)
        return serialRoot

    def serialParallelMap(self):
        nextObj = self.root
        mapping = []
        while nextObj:
            if isinstance(nextObj, ForLoop):
                mapping.append({"parallel": [nextObj.lineNumber, nextObj.endLineNumber]})
            nextObj = nextObj.getNext()

        nextObj = self.serialroot
        counter = 0
        while nextObj:
            if isinstance(nextObj, ForLoop):
                mapping[counter]["serial"] = [nextObj.lineNumber, nextObj.endLineNumber]
                counter += 1
            nextObj = nextObj.getNext()
        return mapping

    def getNestedLoops(self):
        nestedLoopLines = []
        nestedLoopLines = self.root.getNestedLoops(nestedLoopLines, 0)

