import dbManager,logger,os,shutil
import hashlib,dbManager
import gc
import time
from nonarchiFeatureFetcher import hotspotsProfiler

def checkSumAnalyzer(fileInformation):
    availableFiles = []
    allFiles= []
    for fileInfo in fileInformation:
        allFiles.append(fileInfo['fileName'])
    if(dbManager.read('metaDataExists')):
        metaDataSet = dbManager.read('metaData')
        for fileInfo in fileInformation:
            for fileMetaInfo in metaDataSet:
                if(fileInfo['fileName']==fileMetaInfo['fileName']):
                    if(fileInfo['hashValue']==fileMetaInfo['checksumValue']):
                        if not fileMetaInfo['csv']== None:
                            #append data in relevant manner
                            availableFiles.append(fileInfo['fileName'])
                            break
    return list(set(allFiles)-set(availableFiles))




def featureExtractionExecutor(extractor,directory,loopSections,fileNames):
    gpuStartTime = time.time()
    with open(directory + "/_profiling/Sandbox/Makefile", 'r') as file :
        filedata = file.read()
        filedata = filedata.replace('.c', '_serial.c')
    with open(directory + "/_profiling/Sandbox/Makefile", 'w') as file:
        file.write(filedata)
    for fileName in fileNames:
        filePath = directory + "/" + fileName
        fileFeaturePath = directory + "/_profiling/Sandbox/" + fileName
        fileTempPath = filePath.replace("_serial.c",".c")
        sourceObj = extractor.getSource(fileTempPath)
        serialSections = []
        parallelSections = []
        for item in  sourceObj.serialParallelOuterLoopMap():
            for subItem in sourceObj.serialParallelOuterLoopMap()[item]:
                if item == "serial":
                    serialSections.append(str(subItem.lineNumber)+":"+str(subItem.endLineNumber))
                else:
                    parallelSections.append(str(subItem.lineNumber)+":"+str(subItem.endLineNumber))

        for index,element in enumerate(serialSections):
            parallelStartLine = parallelSections[index].split(":")[0]
            parallelEndLine = parallelSections[index].split(":")[1]
            isIn = 'None'
            for data in loopSections:
                #Can have the file Name restrictions if required.
                if(data['startLine'] == str(int(parallelStartLine)-1) ):
                    if (data['endLine'] == parallelEndLine ):
                        if(data['optimiazability']):
                            data['serialStartLine'] = str(int(element.split(":")[0]) - 1)
                            data['serialEndLine']= str(int(element.split(":")[1]) + 1)
                            isIn = 'proceed'
                            break
                        else:
                            isIn = 'notSig'

            if (isIn=='proceed'):
                sequentialStartLine = int(element.split(":")[0]) - 1
                sequentialEndLine =int(element.split(":")[1]) + 1
                fileName = fileName.replace("_serial.c",".c")
                codeName = fileName+":p["+str(data['startLine'])+"-"+str(data['endLine'])+"]"
                folderPath = directory + "/_profiling/Sandbox"
                loopSegments = [[sequentialStartLine,sequentialEndLine]]
                logger.loggerInfo("GPU Feature Extraction Process Initiated for section "+parallelStartLine+":"+parallelEndLine)
                hotspotsProfiler(codeName,fileFeaturePath,fileFeaturePath,folderPath+"/Makefile","",dbManager.read('runTimeArguments'),loopSegments,directory+"/_profiling",False)
                gc.collect()
                logger.loggerSuccess("GPU Feature Extraction Process completed for section "+parallelStartLine+":"+parallelEndLine)
            elif(isIn=='notSig'):
                logger.loggerInfo("Section "+parallelStartLine+":"+parallelEndLine+" is skipped due to low overhead")
            else:
                logger.loggerInfo("Section "+parallelStartLine+":"+parallelEndLine+" is not a parallelable region. Skipped")
        dbManager.write('loopSectionsTemp', loopSections)
        dbManager.write('gpuFeatureTime', time.time() - gpuStartTime)




def gpuAnalzyer(extractor,directory,loopSections):
    fileData =[]
    logger.loggerInfo("Creating sequential files initiated")
    directoryName = directory.split("/")[-1]
    workingDir = directory + "/_profiling/Sandbox"
    if os.path.exists(workingDir):
        shutil.rmtree(workingDir)
    os.makedirs(workingDir)
    for fileModify in os.listdir(directory):
        filePath = directory + "/" + fileModify
        if os.path.isfile(filePath):
            if fileModify.endswith(".c"):
                sourceObj = extractor.getSource(filePath)
                sourceObj.writeToFile(workingDir + "/" + fileModify, sourceObj.root)
                sourceObj.writeToFile(workingDir + "/" + fileModify[:-2] + "_serial.c", sourceObj.serialroot)
                fileInfo = {'fileName':"",'hashValue':""}
                fileInfo['hashValue'] = hashlib.md5((open(workingDir + "/" + fileModify[:-2] + "_serial.c", 'rb')).read()).hexdigest()
                fileInfo['fileName'] = fileModify[:-2] + "_serial.c"
                fileData.append(fileInfo)
            else:
                shutil.copyfile(filePath, workingDir + "/" + fileModify)
    fileSet =  checkSumAnalyzer(fileData)
    featureExtractionExecutor(extractor,directory,loopSections,fileSet)
    logger.loggerSuccess("Sequential file creation completed")
