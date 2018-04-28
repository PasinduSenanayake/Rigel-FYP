from Block import Block

class ForLoop(Block):
    def __init__(self, startIndex, sourceCode):
        blockDetails = self.getBlockLength(sourceCode, startIndex)
        loopHeader = sourceCode[startIndex:blockDetails["blockStartIndex"]]
        elements = [Block(blockDetails["blockStartIndex"], sourceCode[blockDetails["blockStartIndex"]:blockDetails["blockEndIndex"]])]
        super(ForLoop, self).__init__(startIndex, loopHeader)
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

    def isChild(self, parent):
        if parent.getStartIndex() < self.getStartIndex() and self.getStartIndex() < parent.getEndIndex():
            return True
        return False

    def addChild(self, child):
        for i, item in enumerate(self.elements):
            if child.isChild(item):
                if isinstance(item, Block):
                    a = child.getStartIndex() - item.getStartIndex()
                    b = child.getEndIndex() - item.getStartIndex()
                    block1 = Block(item.getStartIndex(), item.body[:a])
                    block2 = child
                    block3 = Block(child.getEndIndex() + 1, item.body[b + 1:])
                    del self.elements[i]
                    self.elements.insert(i, block3)
                    self.elements.insert(i, block2)
                    self.elements.insert(i, block1)
                else:
                    item.addChild(child)
