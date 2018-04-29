from FileHandler import FileHandler
from SourceCode import SourceCode

class Extractor:

    def __init__(self):
        self.sourceCodes = {}

    def addSource(self, sourcePath):
        source = SourceCode(FileHandler.getInstance().readSource(sourcePath))
        self.sourceCodes[sourcePath] = source
        return source

    # def setSchedule(self, sourcePath, mechanism):
    #     self.sourceCodes[sourcePath].setSchedule(mechanism)
    #
    # def writeToFile(self, sourcePath, outPath):
    #     self.sourceCodes[sourcePath].writeToFile(outPath)





