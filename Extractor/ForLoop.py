from Block import Block

class ForLoop(Block):
    def __init__(self, startIndex, sourceCode):
        blockDetails = self.getBlockLength(sourceCode, startIndex)
        loopHeader = sourceCode[startIndex:blockDetails["blockStartIndex"]]
        elements = [Block(sourceCode[blockDetails["blockStartIndex"]:blockDetails["blockEndIndex"]], blockDetails["blockStartIndex"])]
        super(ForLoop, self).__init__(loopHeader, startIndex)
        super(ForLoop, self).setElements(elements)
        self.iterationCount = 0

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

    # def isChild(self, parent):
    #     if parent.getStartIndex() < self.getStartIndex() and self.getStartIndex() < parent.getEndIndex():
    #         return True
    #     return False

    def addChild(self, child):
        for i, item in enumerate(self.elements):
            if child.isChildByIndex(item):
                if isinstance(item, Block):
                    a = child.getStartIndex() - item.getStartIndex()
                    b = child.getEndIndex() - item.getStartIndex()
                    block1 = Block(item.body[:a], item.getStartIndex())
                    block2 = child
                    block3 = Block(item.body[b + 1:], child.getEndIndex() + 1)
                    del self.elements[i]
                    self.addElement(i, block3)
                    self.addElement(i, block2)
                    self.addElement(i, block1)
                else:
                    item.addChild(child)

    # def getNestedLoops(self, loopLines, currentLevel):
    #     currentLevel = currentLevel + 1
    #     newLoopLines = loopLines
    #     if(currentLevel > 1):
    #         return loopLines
    #     elif currentLevel == 1:
    #         for element in self.elements:
    #             newLoopLines = newLoopLines + element.getNestedLoops(newLoopLines,currentLevel)
    #         if len(newLoopLines) == len(loopLines):
    #     return loopLines
