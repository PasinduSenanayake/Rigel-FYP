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
        with open(sourcePath, 'r') as myfile:
            source = myfile.read()
        return source

    def readDirectives(self):
        directiveDataDict = {}
        directivesList = json.load(open("Directives/main.json"))
        directivesList = directivesList["directives"].split(",")
        for directive in directivesList:
            filePath = "Directives/" + directive + ".json"
            directiveData = json.load(open(filePath))
            directiveDataDict[directive] = directiveData
        return directiveDataDict


