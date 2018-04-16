
class ForLoop:
    # def __init__(self, code, startIndex, blockStartIndex, blockEndIndex, iterationCount):
    #     self.code = code
    #     self.startIndex = startIndex
    #     self.r_blockStartIndex = blockStartIndex - startIndex
    #     self.r_blockEndIndex = blockEndIndex - startIndex
    #     self.loopHeader = code[:self.r_blockStartIndex-1]
    #     self.body = code[self.r_blockStartIndex-1:]
    #     self.iterationCount = iterationCount

    def __init__(self, startIndex, sourceCode):
        blockDetails = self.getBlockLength(sourceCode, startIndex)
        self.startIndex = startIndex
        self.loopHeader = sourceCode[startIndex:blockDetails["blockStartIndex"]-1]
        self.body = sourceCode[blockDetails["blockStartIndex"]-1:blockDetails["blockEndIndex"]]
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
        return {"blockStartIndex":blockStartIndex, "blockEndIndex":startIndex+blockLength}