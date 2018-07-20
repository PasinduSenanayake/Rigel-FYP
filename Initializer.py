import os,sys
from Extractor.Extractor import Extractor
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Utils")
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Logger")
from Identifier.initializer  import identify
from Modifier.initializer  import modify
from shutil import copyfile
import shutil,datetime,logger

def processInitializer():
    logger.createLog()
    isMetaDataExists = False
    extractor = None
    directoryList = os.listdir(os.path.dirname(os.path.realpath(__file__))+"/Sandbox")
    if ".gitkeep" in directoryList:
        directoryList.remove(".gitkeep")
    if "metadata" in directoryList:
        isMetaDataExists = True
        directoryList.remove("metadata")

    if not len(directoryList)==1:
        print "There are more than one folder in Sandbox. Please keep only one folder."
        logger.loggerError("There are more than one folder in Sandbox.")
        exit()
    else:

        #Identifier Begins
        logger.loggerInfo("Source Code Identification Process Initiated")
        logger.loggerInfo("Extracting Source Code Initiated")
        sourceDirectry = os.path.dirname(os.path.realpath(__file__))+"/Sandbox/"+directoryList[0]
        extractor = Extractor(sourceDirectry)
        logger.loggerSuccess("Extracting Source Code concluded successfully")

        if(isMetaDataExists):
            logger.loggerInfo("Meta data insertion Initiated")

            logger.loggerSuccess("Meta data insertion Completed")

        identify(extractor,sourceDirectry)

        logger.loggerInfo("Source Code Identification Process Completed Successfully")
        #Identifier Completed

        #Modifier Begins
        logger.loggerInfo("Source Code Modification Process Initiated")
        modify(extractor,sourceDirectry)


processInitializer()
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
