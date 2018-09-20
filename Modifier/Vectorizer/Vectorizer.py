from numpy import vectorize

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
            print(source)
            loopMapping = source.getLoopMapping()
            fileName = filePath.split("/")[-1]
            for vector in vectorList:
                startLine = None
                endLine = None
                for entry in loopMapping["parallel"]:
                    if entry[0] == vector["line"]:
                        startLine = entry[0]
                        endLine = entry[1]
                        break
                if not startLine:
                    for entry in loopMapping["parallel"]:
                        if int(entry[0]) == int(vector["line"]) - 1:
                            logger.loggerInfo(
                                "Exact loop was not found for line number "+ str(vector["line"]) + ". Nearest previous loop considered.")
                            startLine = entry[0]
                            endLine = entry[1]
                            break

                vectorLen = self.getVectorLength(startLine, endLine, filePath, instructionSet)
                if vector["type"] == "vectorized_loop":
                    source.vectorize(vector["line"], vectorLen)
            # source.root.setLineNumber(1)
            print(vectorDirectory + "/" + fileName[:-2] + "_vectorized.c")
            source.writeToFile(vectorDirectory + "/" + fileName[:-2] + "_vectorized.c", source.tunedroot)


    def getLatestInstrucionSet(self):
        systemDetails = dbManager.read("systemData")
        instructionSets = systemDetails["cpuinfo"]["vectorization"]
        for set in reversed(instructionSets):
            if "avx-512" in set:
                logger.loggerInfo(
                    set + " instruction set available for vectorization")
                return set
        for set in reversed(instructionSets):
            if "avx" in set:
                logger.loggerInfo(
                    set + " instruction set available for vectorization")
                return set
        for set in reversed(instructionSets):
            if "sse" in set:
                logger.loggerInfo(
                    set + " instruction set available for vectorization")
                return set

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
            if dataType not in dataSizes:
                logger.loggerInfo("Variable type other than int, float, double found in arrays. Macros not supported. Found type - " + dataType)
                continue
            sizes.append(int(dataSizes[dataType]))
        if len(sizes) == 0:
            logger.loggerInfo(
                "Failed to find valid data types inside the loop. Assuming a size of a double")
            sizes.append(8)

        if (all(x == sizes[0] for x in sizes)):
            for set,length in registerLength.items():
                if set in instructionSet:
                    return registerLength[set]/(sizes[0]*8)
        else:
            for set,length in registerLength.items():
                if set in instructionSet:
                    return registerLength[set] / (max(sizes) * 8)


