import json
from pprint import pprint

class FileHandler:

    instance = None

    @staticmethod
    def getInstance():
        if FileHandler.instance == None:
            FileHandler()
        return FileHandler.instance

    def __init__(self):
        if FileHandler.instance != None:
            return self
        else:
            FileHandler.instance = self

    def readSource(self, sourcePath):
        file = []
        with open(sourcePath, 'r') as myfile:
            for line in myfile:

                file.append(line)

        return file


