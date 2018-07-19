from VectorReportAnalyzer import VectorReportAnalyzer
import os
import sys
from shutil import copyfile
sys.path.append('..')
#import subCommandExecuter
import shutil
import json
import pprint
import os.path

class Vectorizer():
    def __init__(self, extractor, directory):
        instructionSet = self.getLatestInstrucionSet()
        vectorDirectory = directory + "/_vectorization"
        if os.path.exists(vectorDirectory):
            shutil.rmtree(vectorDirectory)
        os.makedirs(vectorDirectory)
        for file in os.listdir(directory):
            filePath = directory + "/" + file
            if os.path.isfile(filePath):
                if not file.endswith(".c"):
                    copyfile(filePath, vectorDirectory + "/" + file)

        sourcePaths = extractor.getSourcePathList()
        self.analyzer = VectorReportAnalyzer(sourcePaths)
        for filePath, vectorList in self.analyzer.vectors.items():

            source = extractor.getSource(filePath)
            loopMapping = source.getLoopMapping()
            fileName = filePath.split("/")[-1]
            for vector in vectorList:
                startLine = vector["line"]
                endLine = None
                for entry in loopMapping["parallel"]:
                    if entry[0] == vector["line"]:
                        endLine = entry[1]
                dataSize = self.getDataSize(startLine, endLine, filePath)
                if vector["type"] == "vectorized_loop":
                    source.vectorize(vector["line"], vector["vectorLen"])
            # source.root.setLineNumber(1)
            source.writeToFile(vectorDirectory + "/" + fileName[:-2] + "_vectorized.c", source.root)


    def getLatestInstrucionSet(self):
        systemDetails = subCommandExecuter.runCommand("systemIdentify")['content']
        instructionSets = systemDetails["cpuinfo"]["vectorization"]
        for set in instructionSets:
            if "avx-512" in set:
                return "avx-512"
        for set in instructionSets:
            if "avx" in set:
                return "avx"
        for set in instructionSets:
            if "sse" in set:
                return "sse"

    def getDataSize(self, startLine, endLine, filePath):
        with open(os.path.dirname(__file__) + '/../subCommandConf.json', 'r+') as fileObj:
            data = json.load(fileObj)
            data["command"]["arrayInfoFetch"]["annotatedFile"] = filePath
            data["command"]["arrayInfoFetch"]["infoFetchStartLine"] = startLine
            data["command"]["arrayInfoFetch"]["infoFetchEndLine"] = endLine
            fileObj.seek(0)
            json.dump(data, fileObj, indent=4)
            fileObj.truncate()
        loopDetails = subCommandExecuter.runCommand("arrayInfoFetch")
        print loopDetails
