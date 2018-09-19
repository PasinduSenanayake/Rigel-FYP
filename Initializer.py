import os,sys
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Utils")
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Logger")
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/DatabaseManager")
from Handler import updateAllInit
from Initialize import moduleInit
from shutil import copyfile
import shutil,datetime,logger


directoryList = []

def processInitializer():
    from Identifier.initializer import identify
    from Extractor.Extractor import Extractor
    from Extractor.metaDataExtractor import metaDataExtractor
    from Modifier.initializer import modify

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

    #Identifier Initiated
    response = identify(extractor, sourceDirectry)
    #Identifier Completed
    if response['returncode'] == 0:
        logger.loggerInfo("Source Code Identification Process Completed Successfully")
        #Modifier Begins
        logger.loggerInfo("Source Code Modification Process Initiated")
        modify(extractor, sourceDirectry)
    else:
        logger.loggerError("Source Code Identification Process Failed. Optimization process terminated.")
        return False

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
