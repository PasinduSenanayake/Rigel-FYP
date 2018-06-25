from subprocess import Popen, PIPE
from os import environ
import xmltodict
import re
import string
import os
from Identifier.offloadChecker import __loadLoopData

#Note: no comment lines should be included in between for loops
#inner loops are not used for collapsing as this may hinder vectorization if available
#loop structures like {A:[B,B]} are not taken in to consideration

# addIntelCPath('/opt/intel/bin/compilervars.sh','intel64')
# compileFile('all')    icc -profile-loops='+profileType+' -profile-loops-report=2 3mmCpu.c -o testCpu
# runFile()
hwdFilepath = str(os.path.dirname((os.path.dirname(os.path.realpath(__file__)))))

print hwdFilepath

allLoopData = {}
sourceCode = []

def readXML(fileName,loopName):
    with open(fileName+'.xml') as fd:
        doc = xmltodict.parse(fd.read())
    loopData ={}
    loopTempData ={}
    for loop in doc['loop_prof']['loops']['loop']:  #iterating over loops in the XML
        loopLine = int(loop['src_file']['line'])    #gets entry line of the loop
        loopSelfTime = int(loop['self_abs'])        #gets time to execute self loop (time of nested loops are not included)
        loopIterations = int(loop['avg_trip_cnt'])  #avg number of iterations

        if loopLine in  loopTempData:
            loopTempData[loopLine]['loopIterations'] = loopTempData[loopLine]['loopIterations'] + loopIterations
            loopTempData[loopLine]['loopSelfTime'] = loopTempData[loopLine]['loopSelfTime'] + loopSelfTime
        else:
            loopTempData[loopLine] = {}
            loopTempData[loopLine]['nestedIterationTime'] = 0
            loopTempData[loopLine]['nestedIterations'] = 1
            loopTempData[loopLine]['collapse'] = [False, False] #[collaspsibleAbove, collapsibleBelow]
            loopTempData[loopLine]['loopIterations'] = loopIterations
            loopTempData[loopLine]['loopSelfTime'] = loopSelfTime
    for line, value in loopTempData.iteritems():
        value['indivdualIterationTime'] = float(float(value['loopSelfTime'])/float(value['loopIterations']))
        loopData[line] = value
    allLoopData[loopName] = loopData


# removes trailing \n from orginal sourceCode
def lineReader():
    global sourceCode
    sourceCode = [line.rstrip('\n') for line in open('3mm.c')] #CfileName


def loopEndFinder(loopStart):
    brackCount = 0
    loopEndLine = 0
    for line in sourceCode[loopStart:]:
        brackCount = brackCount + len(re.findall('{',line))
        brackCount = brackCount - len(re.findall('}',line))
        if(brackCount == 0):
            loopEndline = loopStart + sourceCode[loopStart:].index(line)+1
            break
    return loopEndline




readXML('loop_prof_1527836611','allLoops') #XMLFIleName
lineReader()
loopMetaData = {}
loopOrder = {}
loopOrderParent = {}
loopAlphabet = string.ascii_uppercase
loopKeySet = allLoopData['allLoops'].keys()

#saves loop data with start index and end index of the loop
for key in loopKeySet:
    loopMetaData[loopAlphabet[loopKeySet.index(key)]] = {'loopStart':key,'loopEnd':loopEndFinder(key),'loopMeta':allLoopData['allLoops'][key]}

loopSubAlpahebt = loopAlphabet[:len(loopMetaData)]

for alpha in loopSubAlpahebt:
    for otherAlpha in loopSubAlpahebt[loopSubAlpahebt.index(alpha)+1:]:
        if((loopMetaData[alpha]['loopStart']<loopMetaData[otherAlpha]['loopStart']) & (loopMetaData[alpha]['loopEnd']>loopMetaData[otherAlpha]['loopEnd'])):
            if alpha in loopOrder.keys():
                loopOrder[alpha].append(otherAlpha)
            else:
                loopOrder[alpha] = []
                loopOrder[alpha].append(otherAlpha)
        elif ((loopMetaData[alpha]['loopStart']>loopMetaData[otherAlpha]['loopStart']) & (loopMetaData[alpha]['loopEnd']<loopMetaData[otherAlpha]['loopEnd'])):
            if otherAlpha in loopOrder.keys():
                loopOrder[otherAlpha].append(alpha)
            else:
                loopOrder[otherAlpha] = []
                loopOrder[otherAlpha].append(alpha)

for alpha in loopSubAlpahebt:
    for otherAlpha in loopSubAlpahebt[loopSubAlpahebt.index(alpha)+1:]:
        if((loopMetaData[alpha]['loopStart']>loopMetaData[otherAlpha]['loopStart']) & (loopMetaData[alpha]['loopEnd']<loopMetaData[otherAlpha]['loopEnd'])):
            if alpha in loopOrderParent.keys():
                loopOrderParent[alpha].append(otherAlpha)
            else:
                loopOrderParent[alpha] = []
                loopOrderParent[alpha].append(otherAlpha)
        elif ((loopMetaData[alpha]['loopStart']<loopMetaData[otherAlpha]['loopStart']) & (loopMetaData[alpha]['loopEnd']>loopMetaData[otherAlpha]['loopEnd'])):
            if otherAlpha in loopOrderParent.keys():
                loopOrderParent[otherAlpha].append(alpha)
            else:
                loopOrderParent[otherAlpha] = []
                loopOrderParent[otherAlpha].append(alpha)

nonIndepentSet  = set(loopOrder.keys()+loopOrderParent.keys())
totalSet = set(loopMetaData.keys())


#loopOrder = {'A':['B','C','D','E','F'],'B':['E','F','C','D'],'C':['D'],'E':['F']}
maxVal =  max(len(value) for key,value in loopOrder.iteritems())
valueThresh = 1
while (valueThresh<maxVal):
    loopOrderTemp = loopOrder.copy()
    for key,value in loopOrderTemp.iteritems():
        if(len(value)==valueThresh):
            changed = False
            searchList = [key]+value
            for keyData in loopOrder.keys():
                if all(x in loopOrder[keyData] for x in searchList):
                    changed = True
                    loopOrder[keyData].remove(key)
                    for element in value:
                        loopOrder[keyData].remove(element)
                    loopOrder[keyData].append({key:value})
            if(changed):
                del loopOrder[key]

    valueThresh = valueThresh +1;



def findSemiColon(startIndex,endIndex):
    for line in sourceCode[startIndex:endIndex]:
        if (len(re.findall('{',line)) > 0):
            startIndex = startIndex + sourceCode[startIndex:].index(line)+1
            break
    for line in sourceCode[startIndex:endIndex-1]:
        colonCount = len(re.findall(';', line))
        if(colonCount == 1):
            return False
    else:
        return True



def isCollapsible(loopData):
    global loopMetaData
    for key,value in loopData.iteritems():
        loopStartIndex = loopMetaData[key]['loopStart']
        if len(value)==1:
            for val in value:
                if isinstance(val,dict): # {A:{B:C}}
                    for key1 in val:
                        loopEndIndex = loopMetaData[key1]['loopStart']
                        collapsible = findSemiColon(loopStartIndex,loopEndIndex)
                        loopMetaData[key]["loopMeta"]['collapse'][1] = collapsible
                        loopMetaData[key1]["loopMeta"]["collapse"][0] = collapsible
                    isCollapsible(val)
                else:
                    loopEndIndex = loopMetaData[val]['loopStart']
                    collapsible = findSemiColon(loopStartIndex,loopEndIndex)
                    loopMetaData[key]["loopMeta"]['collapse'][1] = collapsible
                    loopMetaData[val]["loopMeta"]['collapse'][0] = collapsible



# find existence of other statements in between loops
# need to check if final collapsible iteration count is within the range
def findCollapsibleParallelism(loopData):
    global loopMetaData
    for key,value in loopData.iteritems():
        if len(value) == 1:
            if(loopMetaData[key]['loopMeta']['collapse'][1]):
                    if isinstance(value[0], dict):
                        nestedIterations = loopMetaData[key]['loopMeta']['loopIterations'] * findCollapsibleParallelism(value[0])
                        loopMetaData[key]['loopMeta']['nestedIterations'] = nestedIterations
                    else:
                        return loopMetaData[key]['loopMeta']['loopIterations']
            else:
                return loopMetaData[key]['loopMeta']['loopIterations']
                #for val in value:
                    #if isinstance(val,dict):
                        #findCollapsibleParallelism(val)
        else:
            return loopMetaData[key]['loopMeta']['loopIterations']

isCollapsible(loopOrder)
findCollapsibleParallelism(loopOrder)



__loadLoopData(loopOrder, loopMetaData)
