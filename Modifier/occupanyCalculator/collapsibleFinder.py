import fileinput
import sys,os
from subprocess import Popen, PIPE
from shutil import copyfile
global pragmaLine
global compilerOptins
fileLocation = ''
filePath = ''

def addCollapes(loopLine,contentList):
    content = ''
    index = 1
    for line in contentList:
        if index == loopLine:
            content = content + line + "\n#pragma omp for collapse(1)\n"
        else:
            content = content + line
        index = index + 1
    with open(filePath,'w') as out:
        out.write(content)

def runCode():
    processOutput = Popen('cd '+fileLocation +' && clang -c -fopenmp -ferror-limit=1000 '+compilerOptins + ' ' + filePath +
                          ' -o withCollapse',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if "#pragma omp for collapse" in error:
        return error
    else:
        return "success"


def incrementAndRun(numofLoops):
    lines = open(filePath, 'r').readlines()
    for index,line in enumerate(lines):
     if "#pragma omp for collapse" in line:
         code = line
         lines[index] = "#pragma omp for collapse("+str(numofLoops)+") \n"
    out = open(filePath, 'w')
    out.writelines(lines)
    out.close()
    if(runCode()=="success"):
        return incrementAndRun(numofLoops+1)

    else:
        return numofLoops-1


def collapseAnnotator(offloadFilePath,loopStartLine,contentList,compilerOptions=''):
    global compilerOptins
    global  fileLocation
    global filePath
    compilerOptins = compilerOptions
    fileName = "/" + offloadFilePath.rsplit('/', 1)[1]
    fileLocation = offloadFilePath.replace(fileName, "")
    fileName = fileName.split('.c')[0]
    filePath = fileLocation + fileName + '_withCollapse.c'
    addCollapes(loopStartLine, contentList)
    results = runCode()
    if(results=="success"):
        return incrementAndRun(2)
