from numpy import vectorize

from VectorReportAnalyzer import VectorReportAnalyzer
import os
import sys
import copy
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
        self.extractor = extractor
        instructionSet = self.getLatestInstrucionSet()
        self.vectorDirectory = directory + "/_vectorization"
        if os.path.exists(self.vectorDirectory):
            shutil.rmtree(self.vectorDirectory)
        os.makedirs(self.vectorDirectory)
        for file in os.listdir(directory):
            filePath = directory + "/" + file
            if os.path.isfile(filePath):
                copyfile(filePath, self.vectorDirectory + "/" + file)

        sourcePaths = extractor.getSourcePathList()

        self.analyzer = VectorReportAnalyzer(sourcePaths)

    def vectorize(self):
        return


    def initIntelOptimizations(self, filePath, loopRegion):
        unchangedRoot = copy.deepcopy(self.extractor.getSource(filePath).tunedroot)
        vectorList = self.analyzer.vectors[filePath]
        source = self.extractor.getSource(filePath)
        loopMapping = source.getLoopMapping()
        fileName = filePath.split("/")[-1]
        for vector in vectorList:
            if vector["type"] == "partial_loop" and loopRegion[0] <= int(vector["line"]) <= loopRegion[1]:
                source.distribute(vector["line"], vector["section"], vector["permutation"], vector["chunk"])
        for vector in vectorList:
            if (vector["type"] == "permuted_loop" or \
                    (vector["type"] == "partial_loop" and vector["permutation"])) \
                    and loopRegion[0] <= int(vector["line"]) <= loopRegion[1]:
                source.permute(vector["line"], vector["permutation"])
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
            if loopRegion[0] <= startLine <= loopRegion[1]:
                # vectorLen = self.getVectorLength(startLine, endLine, filePath, instructionSet)
                vectorLen = 8
                if vector["permutation"] and not vector["section"] and vector["vectorize"]:
                    stepsBack = len(vector["permutation"][1]) - vector["permutation"][1].index(str(len(vector["permutation"][1]))) - 1
                    source.vectorize(vector["line"], vectorLen, None, vector["chunk"], vector["collapsed"], stepsBack)
                elif vector["vectorize"]:
                    source.vectorize(vector["line"], vectorLen, None, vector["chunk"], vector["collapsed"])
        # source.root.setLineNumber(1)
        source.writeToFile(self.vectorDirectory + "/" + fileName, source.tunedroot)
        from Evaluator.initializer import finalExecutor
        logger.loggerInfo("Test Execution Initiated")
        responseObj = finalExecutor(self.vectorDirectory, dbManager.read('runTimeArguments'))
        if responseObj['returncode'] == 1:
            logger.loggerSuccess("Test Execution completed successfully for vectorizing loop at " + str(loopRegion[0]))
            if not int(dbManager.read('finalExeTime')) < int(dbManager.read('iniExeTime')):
                self.extractor.getSource(filePath).tunedroot = unchangedRoot
                source.writeToFile(self.vectorDirectory + "/" + fileName, source.tunedroot)

        else:
            logger.loggerError(responseObj['error'])
            logger.loggerError("Test Execution FAILED when vectorizing loop at " + str(loopRegion[0]) + ". Optimization process terminated.")
            exit()


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
            found = False
            for dataTypeItr, size in dataSizes.items():
                if dataTypeItr in dataType:
                    sizes.append(size)
                    found = True
                    break
            if not found:
                logger.loggerInfo("Variable type other than int, float, double found in arrays. Macros not supported. Found type - " + dataType)

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


