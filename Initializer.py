import os,sys,json
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Utils")
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Logger")
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/DatabaseManager")
from Handler import updateAllInit
from Initialize import moduleInit
from shutil import copyfile
import shutil,datetime,logger,dbManager

directoryList = []

def processInitializer():
    from Identifier.initializer import identify
    from Extractor.Extractor import Extractor
    from Extractor.metaDataExtractor import metaDataExtractor
    from Modifier.initializer import modify
    from Evaluator.initializer import initExecutor
    #Identifier Begins
    logger.loggerInfo("Extracting Source Code Initiated")
    sourceDirectry = os.path.dirname(os.path.realpath(__file__))+"/Sandbox/"+directoryList[0]
    extractor = Extractor(sourceDirectry)
    logger.loggerSuccess("Extracting Source Code concluded successfully")

    #metaData extraction
    logger.loggerInfo("MetaData extraction Initialized")
    metaDataExtractor()
    logger.loggerSuccess("MetaData extraction Completed")
    #metaData extraction completed

    #Runtime arg extraction Initiated
    logger.loggerInfo("Run time arguments fetcher Initiated")
    with open(sourceDirectry+'/run.json') as runArgumentFile:
        dataArguments = json.load(runArgumentFile)
    if not (dataArguments['runTimeArguments'] == None):
        dbManager.write('runTimeArguments',str(dataArguments['runTimeArguments']))
    else:
        logger.loggerError("Run time arguments fetcher Failed. Optimization process terminated.")
        print "Run time arguments fetcher Failed. Optimization process terminated."
        exit()
    logger.loggerSuccess("Run time arguments fetcher completed successfully")
    #Runtime arg extraction Completed

    #Primary Execution Initiated
    logger.loggerInfo("Primary Execution Initiated")
    responseObj =initExecutor(sourceDirectry,dbManager.read('runTimeArguments'))
    if responseObj['returncode']==1:
        logger.loggerSuccess("Primary Execution completed successfully.")
        print dbManager.read('iniExeTime')
    else:
        logger.loggerError(responseObj['error'])
        logger.loggerError("Primary Execution Failed. Optimization process terminated.")
        exit()
    #Primary Execution Completed

    #Identifier Initiated
    logger.loggerInfo("Source Code Indetification Process Initiated")
    response = identify(extractor, sourceDirectry)
    if response['returncode'] == 0:
        logger.loggerSuccess("Source Code Identification Process Completed Successfully")

    else:
        logger.loggerError("Source Code Identification Process Failed. Optimization process terminated.")
        return False
    #Identifier Completed

    #Modifier Begins
    logger.loggerInfo("Source Code Modification Process Initiated")
    exit()
    modify(extractor, sourceDirectry)
    #Modifier Completed

    #Evaluator Begins
    logger.loggerInfo("Program Evaluation Process Initiated")
    #modify(extractor, sourceDirectry)
    logger.loggerSuccess("Program Evaluation Process Completed Successfully")
    #Evaluator Completed

    return True

def dependencyChecker():
    if(os.path.isfile(os.path.dirname(os.path.realpath(__file__))+'/DatabaseManager/rigel.db')):
        os.remove(os.path.dirname(os.path.realpath(__file__))+'/DatabaseManager/rigel.db')
    if(os.path.isfile(os.path.dirname(os.path.realpath(__file__))+'/DependencyManager/requirementsLocal.json')):
        updateResponse = updateAllInit()
        if(updateResponse):
            logger.loggerSuccess("Dependecies updated")
            return True
        else:
            return False
    else:
        initResponse = moduleInit()
        if(initResponse['code']==0):
            logger.loggerSuccess("Dependecies updated")
            return True
        else:
            logger.loggerError("Dependecies update failed with error : "+initResponse['error'])
            return False

def sourceIntegrityChecker():
    global directoryList
    directoryList = os.listdir(os.path.dirname(os.path.realpath(__file__))+"/Sandbox")
    if ".gitkeep" in directoryList:
        directoryList.remove(".gitkeep")
    if "metadata" in directoryList:
        directoryList.remove("metadata")

    if not len(directoryList)==1:
        print "There are more than one folder in Sandbox. Please keep only one folder."
        logger.loggerError("There are more than one folder in Sandbox.")
        return False
    if len(directoryList)==0:
        print "Required folder is missing in Sandbox."
        logger.loggerError("Required folder is missing in Sandbox.")
        return False
    if not os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/"+directoryList[0]+'/Makefile'):
        print "Makefile is missing."
        logger.loggerError("Makefile is missing.")
        return False
    if not os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/"+directoryList[0]+'/run.json'):
        print "run.json is missing."
        logger.loggerError("run.json is missing.")
        return False
    return True


if __name__ == "__main__":
    logger.createLog()
    logger.loggerInfo("Dependency Validation Process Initiated")
    if(dependencyChecker()):
        logger.loggerSuccess("All Dependencies are Validated")
        logger.loggerInfo("Source Code Integrity Validation Process Initiated")
        if(sourceIntegrityChecker()):
            logger.loggerSuccess("Source Code Validated")
            logger.loggerInfo("Source Code Identification Process Initiated")
            processInitializer()
        else:
            logger.loggerError("Source Code Integrity Validation Failed")
    else:
        logger.loggerError("Dependency Validation Process Falied")



#
# exit()
#
# ### EXTRACTOR ###
# extractor = Extractor(args.fdirectory)
#
#
#
# ##profiling init
# directoryName = args.fdirectory.split("/")[-1]
# workingDir = args.fdirectory + "/_profiling"
# if os.path.exists(workingDir):
#     shutil.rmtree(workingDir)
# os.makedirs(workingDir)
#
# for file in os.listdir(args.fdirectory):
#     filePath = args.fdirectory + "/" + file
#     if os.path.isfile(filePath):
#         if file.endswith(".c"):
#             sourceObj = extractor.getSource(filePath)
#             sourceObj.writeToFile(workingDir + "/" + file, sourceObj.root)
#             sourceObj.writeToFile(workingDir + "/" + file[:-2] + "_serial.c", sourceObj.serialroot)
#         else:
#             copyfile(filePath, workingDir + "/" + file)
#
# ### VECTORIZING ###
#
# vectorizer = Vectorizer(extractor, args.fdirectory)
