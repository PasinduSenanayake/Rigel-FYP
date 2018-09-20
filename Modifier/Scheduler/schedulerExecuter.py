#add static to pragma
#execute and get the results
#extract relevant ones
#run the algorithm
#Inject pragma
import dbManager,logger
import shutil,os
from omppScheduler.omppbasicprofile import getBasicProfile

fileLocation = os.path.dirname(os.path.realpath(__file__))+"/"

def copyFolder(source,destination):
    if os.path.isdir(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)





def getSummary(filePath,runTimeArguments,destination):
    returnResponse = {
    "returncode" :1,
    "content" : [],
    "error" : ""
    }
    response = getBasicProfile(filePath,runTimeArguments)
    if response['returncode'] == 1:
        summarizedReport={}
        dataArray = response['content']
        initLine = dataArray.index('##BEG flat region profiles')
        endLine = dataArray.index('##END flat region profiles')
        loopRegions=[]
        inLoop = False
        for i in range(initLine+1, endLine, 1):
            if not inLoop:
                loopSection = {'startLine':0,'endLine':0}
            if 'flat profile' in dataArray[i]:
                if '##BEG' in dataArray[i]:
                    inLoop = True
                    loopSection['startLine'] = i
                elif '##END' in dataArray[i]:
                    inLoop = False
                    loopSection['endLine'] = i
                    loopRegions.append(loopSection)
        loopSubSets =[]
        for loopSubRegion in loopRegions:
            loopSubSet ={'threadTimes':[],'startLine':'','endLine':'','fileName':'','schedulinMechanism':''}
            for lnum in range(loopSubRegion['startLine']+3,loopSubRegion['endLine']-1):
                loopSubSet['threadTimes'].append(dataArray[lnum].split(',')[3])
            loopMetdata =  dataArray[loopSubRegion['startLine']+1].split(',')
            loopSubSet['startLine'] = loopMetdata[3]
            loopSubSet['endLine'] = loopMetdata[4]
            loopSubSet['fileName'] = loopMetdata[2]
            loopSubSets.append(loopSubSet)

        returnResponse['content'] = loopSubSets
    else:
        returnResponse['content'] = ""
    returnResponse['returncode'] = response['returncode']
    returnResponse['error'] = response['error']
    shutil.rmtree(destination)
    return returnResponse


def mechanismIdentifier(loopInfo):



# def setMechanism(extractor,directory,loopSections):



def schdedulerInitializer(extractor, directory):
    global fileLocation
    copyFolder(directory,fileLocation+'omppScheduler/Sandbox')
    loopContainFiles =[]
    loopSections = dbManager.read('loopSections')
    profiledStatus  = getSummary(directory,dbManager.read('runTimeArguments'),fileLocation+'omppScheduler/Sandbox')
    print profiledStatus
    print loopSections
    exit()
    if (profiledStatus['returncode']==1):
        for singleSection in profiledStatus['content']:
            for indiviualSection in loopSections
            if( singleSection['startLine'] == indiviualSection[''] and singleSection['endLine'] == "" and loopSubSet['fileName']== "" ):
                singleSection = mechanismIdentifier(singleSection)

            #setMechanism(extractor,directory,loopSections)
