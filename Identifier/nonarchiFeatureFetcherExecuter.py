import logger,os,shutil
import hashlib,dbManager


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





def analzyer(extractor,directory):
    fileData =[]
    logger.loggerInfo("Creating sequential files initiated")
    directoryName = directory.split("/")[-1]
    workingDir = directory + "/_profiling"
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
    print "Files Need to profile"
    print checkSumAnalyzer(fileData)
    logger.loggerSuccess("Sequential file creation completed")
