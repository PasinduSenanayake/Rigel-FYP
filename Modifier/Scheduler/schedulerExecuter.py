#add static to pragma
#execute and get the results
#extract relevant ones
#run the algorithm
#Inject pragma
import dbManager,logger
import shutil
from omppScheduler.omppbasicprofile import getBasicProfile

fileLocation = os.path.dirname(os.path.realpath(__file__))+"/"

def copyFolder(source,destination):
    if os.path.isdir(destination):
        os.remove(destination)
     shutil.copytree(source, destination)





def getSummary(filePath,runTimeArguments):
    returnResponse = {
    "returncode" :1,
    "content" : [],
    "error" : ""
    }
    response = getBasicProfile(filePath,runTimeArguments)
    if response['returncode'] == 1:
        summarizedReport={}
        dataArray = response['content']
        print dataArray
    else:
        returnResponse['content'] = ""
    returnResponse['returncode'] = response['returncode']
    returnResponse['error'] = response['error']
    exit()
    return returnResponse


def mechanismIdentifier(loopInfo):



def setMechanism(extractor,directory,loopSections):



def schdedulerInitializer(extractor, directory):
    global fileLocation
    copyfile(directory,fileLocation+'omppScheduler/Sandbox')
    loopContainFiles =[]
    loopSections = dbManager.read('loopSections')
    for loopSection in loopSections:
        if not loopSection['fileName'] in loopContainFiles:
            loopContainFiles.append(loopSection['fileName'])
    for fileName in loopContainFiles:
        newFilePath = fileLocation+'omppScheduler/Sandbox/'+fileName
        profiledStatus  = getSummary(newFilePath,dbManager.read('runTimeArguments'))
        if (profiledStatus['returncode']==1):
            for singleSection in loopSections:
                if(singleSection['loopLines'] in allLoops):
                    singleSection = mechanismIdentifier(singleSection)
            setMechanism(extractor,directory,loopSections)
