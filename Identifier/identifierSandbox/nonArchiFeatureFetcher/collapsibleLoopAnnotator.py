import fileinput
import sys,os
from subprocess import Popen, PIPE
from shutil import copyfile
global pragmaLine
global compilerOptins
fileLocation = os.path.dirname(os.path.realpath(__file__))+"/"

def copyFile(filename):
    copyfile(fileLocation+filename, fileLocation+"withCollapse.c")

def addCollapes():
    lines = open(fileLocation+"withCollapse.c", 'r').readlines()
    for index,line in enumerate(lines):
     if "void profileHook" in line:
         code = line
         lines[index] = code+"#pragma omp for collapse(1) \n"
    out = open(fileLocation+"withCollapse.c", 'w')
    out.writelines(lines)
    out.close()

def makeObjectCode():
    processOutput = Popen('clang -ferror-limit=1000 '+compilerOptins +' '+fileLocation+'withCollapse.c -o '+fileLocation+'runnableSecond',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if error=="":
        return "success"
    else:
        return error

def runCode():
    processOutput = Popen('clang -fopenmp -ferror-limit=1000 '+compilerOptins +' '+fileLocation+'withCollapse.c -o '+fileLocation+'withCollapse',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if error =="":
        return "success"
    else:
        return error

def removePragma():
    lines = open(fileLocation+"withCollapse.c", 'r').readlines()
    for index,line in enumerate(lines):
     if "#pragma omp for collapse" in line:
         lines[index] = " \n"
    out = open(fileLocation+"withCollapse.c", 'w')
    out.writelines(lines)
    out.close()

def captureAndFix(numofLoops):
    processOutput = Popen('clang -fopenmp -ferror-limit=1000 '+compilerOptins +' '+fileLocation+'withCollapse.c -o '+fileLocation+'withCollapse',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    lines = open(fileLocation+"withCollapse.c", 'r').readlines()
    iniIndex = 0
    for index,line in enumerate(lines):
        if "#pragma omp for collapse" in line:
            iniIndex= index
    iniFoundIndex = 0
    for lineIndexInit,line in enumerate(lines[iniIndex:]):
        if "for (" in line:
            numofLoops-=1
            if numofLoops ==1:
                iniFoundIndex = lineIndexInit
                break

    staticIniLineIndex  = 0
    staticIniCharIndex  = 0
    foundString = False
    for lineIndexInit,line in enumerate(lines[(iniIndex+iniFoundIndex):]):
        for charIndex,char in enumerate(line):
            if char == "{":
                staticIniLineIndex = lineIndexInit
                staticIniCharIndex = charIndex
                foundString = True
                break
        if(foundString):
            break
    realIndex = iniIndex+iniFoundIndex+staticIniLineIndex
    strValIni =  lines[realIndex]
    lines[realIndex] = strValIni[0:staticIniCharIndex+1]+"/*"+strValIni[staticIniCharIndex+1:]
    count = 0
    staticLineIndex = 0
    staticCharIndex = 0
    foundString = False
    for lineIndex,line in enumerate(lines[realIndex:]):
        for charIndex,char in enumerate(line):
            if char == "{":
                count+=1
            if char == "}":
                count-=1
                if count == 0:
                    staticLineIndex = lineIndex
                    staticCharIndex = charIndex
                    foundString = True
                    break
        if(foundString):
            break
    strValEnd =  lines[realIndex+staticLineIndex]
    lines[realIndex+staticLineIndex] = strValEnd[0:staticCharIndex]+"*/"+strValEnd[staticCharIndex:]
    out = open(fileLocation+"withCollapse.c", 'w')
    out.writelines(lines)
    out.close()
    removePragma()


def incrementAndRun(numofLoops):
    lines = open(fileLocation+"withCollapse.c", 'r').readlines()
    for index,line in enumerate(lines):
     if "#pragma omp for collapse" in line:
         code = line
         lines[index] = "#pragma omp for collapse("+str(numofLoops)+") \n"
    out = open(fileLocation+"withCollapse.c", 'w')
    out.writelines(lines)
    out.close()
    if(runCode()=="success"):
        incrementAndRun(numofLoops+1)
    else:
        captureAndFix(numofLoops)

def removeFiles():
    os.remove(fileLocation+'withCollapse')


def collapseAnnotator(fileName,compilerOptions):
    global compilerOptins
    compilerOptins = compilerOptions
    try:
        copyFile(fileName)
        addCollapes()
        results = runCode()
        if(results=="success"):
            incrementAndRun(2)
            results = makeObjectCode()
            if(results=="success"):
                removeFiles()
                return "success"
            else:
                return results
        else:
            removePragma()
            return results

    except Exception as e:
        return str(e)
