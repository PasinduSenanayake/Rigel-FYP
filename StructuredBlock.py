from Block import Block
from Directive import Directive
from ForLoop import ForLoop
import re

class StructuredBlock(Block):
    def __init__(self, directive, associatedLoop, forLoops, sourceCode):
        elements = []
        if(directive):
            elements.append(directive)
            super(StructuredBlock, self).__init__(directive.getStartIndex(), "")
            if(not associatedLoop):
                directiveEndIndex = directive.startIndex + directive.length()
                if(directive.details["general"]["type"] == "BasicStructured"):
                    blockDetails = self.getBlockLength(sourceCode, directiveEndIndex)
                    elements.append(Block(blockDetails["blockStartIndex"], sourceCode[blockDetails["blockStartIndex"]:blockDetails["blockEndIndex"]]))
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
            super(StructuredBlock, self).__init__(associatedLoop.getStartIndex(), "")
        super(StructuredBlock, self).setElements(elements)

    def directive(self):
        if(isinstance(self.elements[0], Directive)):
            return self.elements[0]
        return None

    def isChild(self, parent):
        if parent.getStartIndex() < self.getStartIndex() and self.getStartIndex() < parent.getEndIndex():
            return True
        return False

    def addChild(self, child):
        for i, item in enumerate(self.elements):
            if child.isChild(item):
                if isinstance(item, StructuredBlock) or isinstance(item, ForLoop):
                    item.addChild(child)
                else:
                    a = child.getStartIndex() - item.getStartIndex()
                    b = child.getEndIndex() - item.getStartIndex()
                    # print item.body[:a]
                    # print "-"
                    # print item.body[a:a + b - 1]
                    # print "-"
                    # print item.body[a + b - 1:]
                    # print "-----"

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

