import os,sys
from Extractor.Extractor import Extractor
from Vectorizer.Vectorizer import Vectorizer
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Utils")
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Logger")
from Identifier.ini  import trigger
from shutil import copyfile
import shutil,datetime,logger

def processInitializer():
    logger.createLog()
    extractor = None
    directoryList = os.listdir(os.path.dirname(os.path.realpath(__file__))+"/Sandbox")
    if ".gitkeep" in directoryList:
        directoryList.remove(".gitkeep")
    if "metadata" in directoryList:
        directoryList.remove("metadata")

    if not len(directoryList)==1:
        print "There are more than one folder in Sandbox. Please keep only one folder."
        logger.loggerError("There are more than one folder in Sandbox.")
        exit()
    else:
        logger.loggerInfo("Source Code Identification Process Initiated")
        if (os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json")):
            os.remove(os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json"))
        shutil.copyfile(os.path.dirname(os.path.realpath(__file__))+"/subCommandConfSample.json",os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json")

        logger.loggerInfo("Extracting Source Code Initiated")
        extractor = Extractor(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/"+directoryList[0])
        logger.loggerSuccess("Extracting Source Code concluded successfully")

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
