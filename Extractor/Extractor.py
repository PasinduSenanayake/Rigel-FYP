from FileHandler import FileHandler
from SourceCode import SourceCode
import os

class Extractor:

    def __init__(self, directory):
        self.sourceCodes = {}
        for file in os.listdir(directory):
            filePath = directory + "/" + file
            if os.path.isfile(filePath):
                if file.endswith(".c"):
                    self.addSource(filePath)

    def addSource(self, sourcePath):
        source = SourceCode(FileHandler.getInstance().readSource(sourcePath))
        self.sourceCodes[sourcePath] = source
        return source

    def getSource(self, filePath):
        return self.sourceCodes[filePath]

    def getSourcePathList(self):
        return self.sourceCodes.keys()

    # def setSchedule(self, sourcePath, mechanism):
    #     self.sourceCodes[sourcePath].setSchedule(mechanism)
    #
    # def writeToFile(self, sourcePath, outPath):
    #     self.sourceCodes[sourcePath].writeToFile(outPath)
