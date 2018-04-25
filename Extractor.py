from FileHandler import FileHandler
from SourceCode import SourceCode

class Extractor:

    def __init__(self):
        self.sourceCodes = {}

    def addSource(self, sourcePath):
        self.sourceCodes[sourcePath] = SourceCode(FileHandler.getInstance().readSource(sourcePath))




