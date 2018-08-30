from VectorReportAnalyzer import VectorReportAnalyzer
import os
import sys
from shutil import copyfile
from ..modifierSandbox.arrayInfoIdentifier.arrayInfoExtractor import arrayInfoExtract
import shutil
import json
import pprint
import os.path
import logger
import dbManager

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
                vectorLen = self.getVectorLength(startLine, endLine, filePath, instructionSet)
                if vector["type"] == "vectorized_loop":
                    source.vectorize(vector["line"], vectorLen)
            # source.root.setLineNumber(1)
            source.writeToFile(vectorDirectory + "/" + fileName[:-2] + "_vectorized.c", source.root)


    def getLatestInstrucionSet(self):
        systemDetails = dbManager.read("systemData")
        instructionSets = systemDetails["cpuinfo"]["vectorization"]
        for set in instructionSets:
            if "avx-512" in set:
                logger.loggerInfo(
                    "avx-512 instruction set available for vectorization")
                return "avx-512"
        for set in instructionSets:
            if "avx" in set:
                logger.loggerInfo(
                    "avx instruction set available for vectorization")
                return "avx"
        for set in instructionSets:
            if "sse" in set:
                logger.loggerInfo(
                    "sse instruction set available for vectorization")
                return "sse"

    def getVectorLength(self, startLine, endLine, filePath, instructionSet):
        logger.loggerInfo("Array Information Fetcher Initiated for lines " + str(startLine)+ "-" + str(endLine) )
        response = arrayInfoExtract(filePath,startLine,endLine)
        loopDetails = None
        if(response['code']==0):
            loopDetails = response['content']
        else:
            logger.loggerError("Array Information Fetcher Failed for lines " + str(startLine) + "-" + str(endLine) +" with error " + str(response['error']))
            exit()
        logger.loggerSuccess("Array Information Fetcher Completed Successfully for lines " + str(startLine)+ "-" + str(endLine))
        dataSizes = {"int": 4, "float": 4, "double": 8}
        registerLength = {"sse": 128, "avx": 256, "avx-512": 512}
        sizes = []
        for array, details in loopDetails.items():
            dataType = details["dataType"].replace("*","").strip()
            sizes.append(int(dataSizes[dataType]))
        if (all(x == sizes[0] for x in sizes)):
            return registerLength[instructionSet]/(sizes[0]*8)
        else:
            return registerLength[instructionSet]/(max(sizes)*8)

