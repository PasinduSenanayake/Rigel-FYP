import dbManager,logger
import shutil,os,time
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
            loopSubSet ={'threadTimes':[],'startLine':'','endLine':'','fileName':'','schedulingMechanism':None}
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
    if (maxTime-minTime)/avgTime > 1:
        voting[2] = 1
    else:
        voting[2] = 0
    if sum(voting)> 1:
        sectionTimes=[]
        difAbsVal = 0
        gCounter = 0
        gRCounter = 0
        for count in range(0,len(loopInfo['threadTimes'])-1):
            difAbsVal = difAbsVal + abs(loopInfo['threadTimes'][count+1]-loopInfo['threadTimes'][count])
            sectionTimes.append(loopInfo['threadTimes'][count+1]-loopInfo['threadTimes'][count])
        totalAverage = difAbsVal/(len(loopInfo['threadTimes'])-1)
        for counter in range(0,len(loopInfo['threadTimes'])-1):
            if ((sectionTimes[counter]/totalAverage)>0.5):
                gCounter=gCounter+1
            elif ((sectionTimes[counter]/totalAverage)<-0.5):
                gRCounter=gRCounter+1
        if (float(gCounter)/float(len(loopInfo['threadTimes'])-1) >= 0.6):
            print "guided"
            loopInfo['schedulingMechanism']="guided"
        elif (float(gRCounter)/float(len(loopInfo['threadTimes'])-1)>= 0.6):
            print "guided"
            loopInfo['schedulingMechanism']="guided"
        else:
            print "dynamic"
            loopInfo['schedulingMechanism']="dynamic"
    else:
        print "static"
        loopInfo['schedulingMechanism']="static"



def setMechanism(extractor,directory,loopSections):
    copyFolder(directory,fileLocation+'omppScheduler/Sandbox')
    tempLoopList = []
    for loopSection in loopSections:
        if(loopSection['schedulingMechanism'] != None):
            tempLoopList.append(loopSection['startLine'])
            sourceObj = extractor.getSource(directory+"/"+loopSection['fileName'])
            sourceObj.setSchedule(loopSection['schedulingMechanism'],loopSection['startLine'])
            with open(fileLocation+'omppScheduler/Sandbox/'+loopSection['fileName']) as f:
                file_str = f.readlines()
                file_str[int(loopSection['startLine'])-1] =   file_str[int(loopSection['startLine'])-1].replace('static',loopSection['schedulingMechanism'])
            with open(fileLocation+'omppScheduler/Sandbox/'+loopSection['fileName'], "w") as f:
                f.writelines(file_str)
            #sourceObj.writeToFile(fileLocation+'omppScheduler/Sandbox/'+loopSection['fileName'],sourceObj.tunedroot)
            #sourceObj.writeToFile('/media/pasindu/newvolume/FYP/Framework/Rigel-FYP/Sandbox/2MM/test.c',sourceObj.tunedroot)
    summaryLoops = dbManager.read('summaryLoops')
    profiledStatus  = getSummary(fileLocation+'omppScheduler/Sandbox',dbManager.read('runTimeArguments'),fileLocation+'omppScheduler/Sandbox')
    for profiledLoop in profiledStatus['content']:
        if profiledLoop['startLine'] in tempLoopList :
            for summaryLoop in summaryLoops:
                if( summaryLoop['startLine'] == profiledLoop['startLine'] and summaryLoop['endLine'] == profiledLoop['endLine'] and summaryLoop['fileName']== profiledLoop['fileName'] ):
                    summaryLoop['optimizedTime'] = max(profiledLoop['threadTimes'])
    dbManager.overWrite('summaryLoops',summaryLoops)
    shutil.rmtree(fileLocation+'omppScheduler/Sandbox')

def schdedulerInitializer(extractor, directory):
    global fileLocation
    loopSections = dbManager.read('loopSections')
    schedulerStartTime = time.time()
    profiledStatus  = getSummary(directory,dbManager.read('runTimeArguments'),fileLocation+'omppScheduler/Sandbox')
    if (profiledStatus['returncode']==1):
        for singleSection in profiledStatus['content']:
            for indiviualSection in loopSections:
                if(indiviualSection['optimizeMethod']==None):
                    if( indiviualSection['startLine'] == singleSection['startLine'] and indiviualSection['endLine'] == singleSection['endLine'] and indiviualSection['fileName']== singleSection['fileName'] ):
                        singleSection = mechanismIdentifier(singleSection)
                        break

        setMechanism(extractor,directory,profiledStatus['content'])
    dbManager.write('schedulerExeTime',time.time()-schedulerStartTime)
