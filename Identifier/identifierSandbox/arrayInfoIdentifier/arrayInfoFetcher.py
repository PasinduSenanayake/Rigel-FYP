# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import re,os
from shutil import copyfile

undefinedVariables = {}

fileLocationNew = os.path.dirname(os.path.realpath(__file__))+'/Sandbox'

#Identify the pointer variables in the code
def findVariableTypeAttempt1(fileName,loopStartLine):
    with open(fileLocationNew+fileName) as fin, open(fileLocationNew+'targetChanged1.c', 'w') as fout:
        for i, item in enumerate(fin, 1):
            if i == loopStartLine:
                for key in undefinedVariables.keys():
                    item = item + 'printf("%p",'+key+');\n'
            fout.write(item)
    processOutput = Popen('clang -c '+fileLocationNew+'targetChanged1.c -o '+fileLocationNew+'targetChanged1.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        line = processOutput.stderr.readline()
        if line != '':
            lineCode = line.rstrip()
            if('warning:' in lineCode):
                variableType  = re.findall(r"'\s*([^']+?)\s*'", lineCode)[1]
                nextLine =  processOutput.stderr.readline()
                undefinedVariables[re.search(r'\((.*?)\)',nextLine).group(1).split(',')[1]]['dataType'] = variableType
        else:
            break


def findVariableTypeAttempt2(fileName,loopStartLine):
    with open(fileLocationNew+fileName) as fin, open(fileLocationNew+'targetChanged2.c', 'w') as fout:
        for i, item in enumerate(fin, 1):
            if i == loopStartLine:
                for key in undefinedVariables.keys():
                    item = item + 'printf("%f",'+key+');\n'
            fout.write(item)
    processOutput = Popen('clang -c '+fileLocationNew+'targetChanged2.c -o '+fileLocationNew+'targetChanged2.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        line = processOutput.stderr.readline()
        if line != '':

            lineCode = line.rstrip()
            if('warning:' in lineCode):
                variableType  = re.findall(r"'\s*([^']+?)\s*'", lineCode)[1]
                nextLine =  processOutput.stderr.readline()
                undefinedVariables[re.search(r'\((.*?)\)',nextLine).group(1).split(',')[1]]['dataType'] = variableType
        else:
            break

def findMatrixDimention(matrixDimension,lineCodeStriped,checkIndex,dimenConst):
        if(lineCodeStriped[checkIndex] == '['):
            matrixDimension +=1
            letterCount = 1
            startInner = checkIndex+1
            for index,letter in enumerate(lineCodeStriped[(checkIndex+1):]):
                if letter =='[':
                    letterCount +=1
                if letter == ']':
                    letterCount +=-1
                if letterCount == 0:
                    checkIndex = checkIndex+index+2
                    break
            if lineCodeStriped[startInner:checkIndex].isdigit():
                dimenConst.append('constant')
            else:
                dimenConst.append('variable')
            matrixDimension =findMatrixDimention(matrixDimension,lineCodeStriped,checkIndex,dimenConst)
        return matrixDimension

def findVariablesWithArray(errorArray,loopStartLine,lineCount):
        variable = ""
        errorCodeLine = ""
        errorCodeLineFormer = ""
        variableBeginChar = 0
        for error in errorArray:

            line = error['errorData']
            lineCode = line.rstrip()
            errorLineName = error['errorName']
            errorLineName = errorLineName.rstrip()
            errorCodeLine = errorLineName.split(":")[1]
            variable =  re.findall(r"'(.*?)'", errorLineName, re.DOTALL)[0]
            lineCode = line.rstrip()
            lineCodeStriped = lineCode.strip()
            if (errorCodeLine == errorCodeLineFormer ):
                lineCodeStriped = lineCodeStriped[variableBeginChar:]
            variableIndex = re.search(r''+variable+'', lineCodeStriped)
            variableBeginChar = variableIndex.end()
            checkIndex = variableIndex.end()
            dimenConst = []
            matrixDimension = findMatrixDimention(0,lineCodeStriped,checkIndex,dimenConst)
            if not matrixDimension == 0:
                if not variable in undefinedVariables.keys():
                    undefinedVariables[variable] = {
                    'dataType':'',
                    'segmantData':[]
                    }
                data = {
                    'arrayDimension':matrixDimension,
                    'codeLine':loopStartLine+(int(errorCodeLine)-lineCount)
                     }
                undefinedVariables[variable]['segmantData'].append(data)
                for index,dimen in enumerate(dimenConst):
                    undefinedVariables[variable][str(index+1)+'D'] = dimen
            errorCodeLineFormer = errorCodeLine



def findVariables(fileName,loopStartLine,loopEndline):
    lineCount = 0
    with open(fileLocationNew+fileName) as fin, open(fileLocationNew+'target.c', 'w') as fout:
        for i, item in enumerate(fin, 1):
            if '#include' in item:
                fout.write(item)
                lineCount +=1
            if (i == loopStartLine):
                fout.write('int main() { \n /////######################################################///// \n')
                lineCount = lineCount+2
            if (i > loopStartLine) and (i < loopEndline) :
                fout.write(item)
            if (loopEndline - i == 1):
                fout.write(' /////----------------------------------------------------///// \n}')
    processOutput = Popen('clang -c -ferror-limit=1000 '+fileLocationNew+'target.c -o '+fileLocationNew+'target.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    errorCodeLine = ""
    errorList = []
    errorArray = []
    nextLineUseful = False
    while True:
        line = processOutput.stderr.readline()
        if line != '':

            lineCode = line.rstrip()
            if(nextLineUseful):
                errorList.append({'position':int(errorCodeLine.split(":")[1])*100000+int(errorCodeLine.split(":")[2]),'errorName':errorCodeLine,'errorData':lineCode})
                nextLineUseful = False
            if('use of undeclared identifier' in lineCode):
                nextLineUseful = True

                errorCodeLine = lineCode
                variable =  re.findall(r"'(.*?)'", lineCode, re.DOTALL)[0]
        else:
            break
    errorArray = sorted(errorList, key=lambda k: k['position'])
    findVariablesWithArray(errorArray,loopStartLine,lineCount)

def arrayInfoFetch(fileName,loopStartLine,loopEndline):
    global fileLocationNew
    fileLocationNew = os.path.dirname(os.path.realpath(__file__))+'/Sandbox'
    fileLocationNew = fileLocationNew+fileName.rsplit('/', 1)[0]+"/"
    fileName = "/"+fileName.rsplit('/', 1)[1]
    findVariables(fileName,loopStartLine,loopEndline)
    findVariableTypeAttempt1(fileName,loopStartLine)
    findVariableTypeAttempt2(fileName,loopStartLine)

    isSuccess = True
    # Remove intermediate files
    if (os.path.isfile(fileLocationNew+'target.c')):
        os.remove(fileLocationNew+'target.c')
    else:
        isSuccess = False
    if (os.path.isfile(fileLocationNew+'targetChanged1.c')):
        os.remove(fileLocationNew+'targetChanged1.c')
    else:
        isSuccess = False
    if (os.path.isfile(fileLocationNew+'targetChanged2.c')):
        os.remove(fileLocationNew+'targetChanged2.c')
    else:
        isSuccess = False
    return {'code':isSuccess, 'data':undefinedVariables}
