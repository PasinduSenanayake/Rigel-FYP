import re
import sys
from collections import OrderedDict
regexes = [ re.compile(p) for p in [ 'for','while']]
keywords =  ['for','while','main','printf','omp_get_thread_num','if']
fileDictionary = OrderedDict()
with open(sys.argv[1]) as f:
    for num, line in enumerate(f, 1):
        fileDictionary[num] = line
parallelSections = 0

def isItFunction(startLine, dictionary):
    if (re.search("{",dictionary[startLine+1])):
        return True
    else:
        return False


def subFunctionAnalysis(startLine, endLine, dictionary):
    fuctionSupports = {}
    skippers = {}
    skippers['for'] = []
    skippers['while']=[]
    for num,line in dictionary.iteritems():
        if(startLine < num <= endLine):
            if re.search("[\w]\s*(?=\().+\)|[\w]+(?=\().+\)",line):
                for regex in regexes:
                    if regex.search(re.findall("[\w]+\s+(?=\().+\)|[\w]+(?=\().+\)|[\w]\s*(?=\().+\)|[\w]+(?=\().+\)",line)[0]):
                        if "printf" in line:
                            pass
                        else:
                            tempNum = num
                            parameters = {}
                            for numInside,lineInside in dictionary.iteritems():
                                if(startLine <= numInside <= endLine):
                                    if (tempNum > numInside ):
                                        if(numInside in skippers[regex.pattern]):
                                            continue
                                        else:
                                            if re.search("#pragma omp .*"+ regex.pattern+"|# pragma omp .*"+ regex.pattern,lineInside):
                                                tempNum = numInside
                                                skippers[regex.pattern].append(tempNum)
                                                parameters = {}
                                                variablesInside =  re.findall(".*?\((.*?)\)", dictionary[numInside])
                                                for index, item in enumerate(re.findall("(.*?)\s*\(", dictionary[numInside])):
                                                     parameters[item.rsplit(None, 1)[-1]] = variablesInside[index]
                                    else:
                                        break
                            fuctionSupports[regex.pattern] = parameters
                            print fuctionSupports


                temp = re.findall("(.*?)\s*\(", line)[0]
                for mainNum,mainLine in fileDictionary.iteritems():
                    if temp.rsplit(None, 1)[-1] not in keywords:
                        if re.search("(?:^|\W)"+temp.rsplit(None, 1)[-1]+"(?:$|\W)",mainLine):
                            if(isItFunction(mainNum, fileDictionary)):
                                sectionInspect(OrderedDict((key, value) for key, value in fileDictionary.items() if key > mainNum),"#pragma omp .*|# pragma omp .*")






def sectionInspect(dictionary,regexString,initate = False):
    metaData = {}
    startFlag = 0
    bracketCount = -1
    startLine = 0
    endLine = 0
    for num,line in dictionary.iteritems():
        if(startFlag == 0):
            if re.search(regexString,line):
                startLine = num
                startFlag += 1
        if(startFlag ==1 ):
            if(re.search("{",line)):
                startFlag += 1

        if(startFlag == 2 ):
            if(re.search("}",line)):
                if(bracketCount == 0):
                    endLine = num
                    bracketCount = -1
                    if(initate):
                        global parallelSections
                        parallelSections += 1
                        print parallelSections
                    break
                else:
                    bracketCount -= 1
            if(re.search("{",line)):
                    bracketCount += 1

    if(startFlag == 2):
        subFunctionAnalysis(startLine,endLine,OrderedDict((key, value) for key, value in fileDictionary.items() if endLine > key > startLine-1))
        if(initate):
            variables =  re.findall(".*?\((.*?)\)", dictionary[startLine])
            for index, item in enumerate(re.findall("(.*?)\s*\(", dictionary[startLine])):
                 metaData[item.rsplit(None, 1)[-1]] = variables[index]
            print metaData
            return endLine

    else:
        return len(fileDictionary)


Terminate = False
sectionStartLine = 0
while not Terminate:
    sectionStartLine = sectionInspect(OrderedDict((key, value) for key, value in fileDictionary.items() if key > sectionStartLine),"# pragma omp parallel|#pragma omp parallel",True)
    if(sectionStartLine == len(fileDictionary)):
        Terminate = True
