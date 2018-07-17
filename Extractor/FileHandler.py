import json
from pprint import pprint
import os
import codecs

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
        with codecs.open(sourcePath, 'r', 'utf-8') as myfile:
            source = myfile.read()
        return source

    def readDirectives(self):
        directiveDataDict = {}
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'Directives/main.json')
        directivesList = json.load(open(filename))
        directivesList = directivesList["directives"].split(",")
        for directive in directivesList:
            filePath = os.path.join(dirname, "Directives/" + directive + ".json")
            directiveData = json.load(open(filePath))
            directiveDataDict[directive] = directiveData
        return directiveDataDict


