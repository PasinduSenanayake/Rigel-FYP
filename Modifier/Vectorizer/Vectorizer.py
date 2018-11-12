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
from Evaluator.initializer import finalExecutor

class Vectorizer():
    def __init__(self, extractor, directory):
        self.extractor = extractor
        self.instructionSet = self.getLatestInstrucionSet()
        self.cacheLineSize = "64"
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
        # print(self.analyzer.vectors)

    def addVectorizableLoop(self, line, filePath, region):
        identified = False
        for vector in self.analyzer.vectors[filePath]:
            if int(region[0]) <= int(vector["line"]) <= int(region[1]):
                identified = True
        if not identified:
            self.analyzer.vectors[filePath].append({"line": int(line), "type": "vectorized_loop",
                                                    "vectorize": True, "chunk": None, "section": [line],
                                                    "collapsed": None, "permutation": None})

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
            # print("----")
            # print(loopRegion)
            # print(startLine)
            # print("----")
            if int(loopRegion[0]) <= int(startLine) <= int(loopRegion[1]):
                response = self.getVectorLength(startLine, endLine, filePath, self.instructionSet, source)
                vectorLen = response[0]
                alignedArrays = response[1]
                if vector["permutation"] and not vector["section"] and vector["vectorize"]:
                    stepsBack = len(vector["permutation"][1]) - vector["permutation"][1].index(str(len(vector["permutation"][1]))) - 1
                    source.vectorize(vector["line"], vectorLen, self.cacheLineSize, vector["chunk"], vector["collapsed"], stepsBack, alignedArrays)
                elif vector["vectorize"]:
                    source.vectorize(vector["line"], vectorLen, self.cacheLineSize, vector["chunk"], vector["collapsed"], alignedArrays=alignedArrays)
        # source.root.setLineNumber(1)
        source.writeToFile(self.vectorDirectory + "/" + fileName, source.tunedroot)
        logger.loggerInfo("Test Execution Initiated")
        responseObj = finalExecutor(self.vectorDirectory, dbManager.read('runTimeArguments'), " -m"+self.instructionSet)
        if responseObj['returncode'] == 1:
            logger.loggerSuccess("Test Execution completed successfully for vectorizing loop at " + str(loopRegion[0]))
            if not dbManager.read('finalExeTime') < dbManager.read('iniExeTime'):
                logger.loggerInfo(
                    "vectorization reversed for loop region " + str(loopRegion[0]) + "; seems inefficient")
                self.extractor.getSource(filePath).tunedroot = unchangedRoot
                source.writeToFile(self.vectorDirectory + "/" + fileName, source.tunedroot)
            else:
                logger.loggerSuccess(
                    "vectorization commited for loop region " + str(loopRegion[0]))

                dbManager.overWrite('iniExeTime', dbManager.read('finalExeTime'))
        else:
            logger.loggerError(responseObj['error'])
            logger.loggerError(responseObj['content'])
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

    def getVectorLength(self, startLine, endLine, filePath, instructionSet, source):
        logger.loggerInfo("Array Information Fetcher Initiated for lines " + str(startLine)+ "-" + str(endLine) )
        response = arrayInfoExtract(filePath,startLine,endLine)
        alignedArrays = []
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
                    source.align(array, self.cacheLineSize, dataTypeItr)
                    logger.loggerSuccess("Aligned array " + array)
                    alignedArrays.append(array)
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
            for set, length in registerLength.items():
                if set in instructionSet:
                    return [registerLength[set]/(sizes[0]*8), alignedArrays]
        else:
            for set, length in registerLength.items():
                if set in instructionSet:
                    return [registerLength[set] / (max(sizes) * 8), alignedArrays]

    def optimizeAffinity(self, filePath, loopRegion):
        options = ["master", "close", "spread"]
        currentBest = copy.deepcopy(self.extractor.getSource(filePath).tunedroot)
        fileName = filePath.split("/")[-1]
        source = self.extractor.getSource(filePath)
        for option in options:
            source.addClause(int(loopRegion[0]), "proc_bind", option)
            source.writeToFile(self.vectorDirectory + "/" + fileName, source.tunedroot)
            logger.loggerInfo("Test Execution Initiated after adding affinity clause")
            responseObj = finalExecutor(self.vectorDirectory, dbManager.read('runTimeArguments'),
                                        "-m" + self.instructionSet)
            if responseObj['returncode'] == 1:
                logger.loggerSuccess(
                    "Test Execution completed successfully for adding affinity clause at " + str(loopRegion[0]))
                if not dbManager.read('finalExeTime') < dbManager.read('iniExeTime'):
                    logger.loggerInfo(
                        "thread affinity reversed for directive at " + str(loopRegion[0]) + "; seems inefficient")
                    source.tunedroot = currentBest
                    source.writeToFile(self.vectorDirectory + "/" + fileName, source.tunedroot)
                else:
                    logger.loggerSuccess(
                        "Thread affinity commited for loop region " + str(loopRegion[0]))
                    currentBest = source.tunedroot
                    source.writeToFile(self.vectorDirectory + "/" + fileName, currentBest)
                    dbManager.overWrite('iniExeTime', dbManager.read('finalExeTime'))


