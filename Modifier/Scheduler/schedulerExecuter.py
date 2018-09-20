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
            loopSubSet ={'threadTimes':[],'startLine':'','endLine':'','fileName':'','schedulingMechanism':''}
            for lnum in range(loopSubRegion['startLine']+3,loopSubRegion['endLine']-1):
                loopSubSet['threadTimes'].append(float(dataArray[lnum].split(',')[3]))
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
    #stage 1 selection
    voting = [0,0,0]
    minTime = min(loopInfo['threadTimes'])
    maxTime = max(loopInfo['threadTimes'])
    avgTime = sum(loopInfo['threadTimes'])/int(len(loopInfo['threadTimes']))
    if (avgTime-minTime)/avgTime > 0.5:
        voting[0] = 1
    else:
        voting[0] = 0
    if (maxTime-avgTime)/avgTime > 0.5:
        voting[1] = 1
    else:
        voting[1] = 0
    if (maxTime-minTime)/avgTime > 0.5:
        voting[2] = 1
    else:
        voting[2] = 0
    if sum(voting)> 1:
        print "Non-static"
    else:
        print "Static"
        loopInfo['schedulingMechanism']="static"



# def setMechanism(extractor,directory,loopSections):



def schdedulerInitializer(extractor, directory):
    global fileLocation
    copyFolder(directory,fileLocation+'omppScheduler/Sandbox')
    loopSections = dbManager.read('loopSections')
    profiledStatus  = getSummary(directory,dbManager.read('runTimeArguments'),fileLocation+'omppScheduler/Sandbox')
    if (profiledStatus['returncode']==1):
        for singleSection in profiledStatus['content']:
            for indiviualSection in loopSections:
                if( indiviualSection['startLine'] == singleSection['startLine'] and indiviualSection['endLine'] == singleSection['endLine'] and indiviualSection['fileName']== singleSection['fileName'] ):
                    singleSection = mechanismIdentifier(singleSection)
                    break

            #setMechanism(extractor,directory,loopSections)
