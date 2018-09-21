import fileinput
import sys,os
from subprocess import Popen, PIPE
from shutil import copyfile
global pragmaLine
global compilerOptins
fileLocation = ''


def copyFile(filename):
    copyfile(fileLocation+filename, fileLocation+"withCollapse.c")


def reenableLimit():
    lines = open(fileLocation+"withCollapse.c", 'r').readlines()
    # for index,line in enumerate(lines):
    #     if "/*iteratotConuter++; if(iteratotConuter>100){break;};*/"in line:
    #         lines[index] = line.replace("/*iteratotConuter++; if(iteratotConuter>100){break;};*/","iteratotConuter++; if(iteratotConuter>100){break;};")

    out = open(fileLocation+"withCollapse.c", 'w')
    out.writelines(lines)
    out.close()

def addCollapes(loopLine):
    lines = open(fileLocation+"withCollapse.c", 'r').readlines()
    for index,line in enumerate(lines):
        if index == loopLine-1:
            lines[index] = line+"\n #pragma omp for collapse(1) \n"
        # if "/*dontErase*/ iteratotConuter++; if(iteratotConuter>100){break;};"in line:
        #     lines[index] = line.replace("/*dontErase*/ iteratotConuter++; if(iteratotConuter>100){break;};","/*iteratotConuter++; if(iteratotConuter>100){break;};*/")
    out = open(fileLocation+"withCollapse.c", 'w')
    out.writelines(lines)
    out.close()



def runCode():
    processOutput = Popen('cd '+fileLocation +' && clang -c -fopenmp -ferror-limit=1000 '+compilerOptins +' '+fileLocation+'withCollapse.c -o '+fileLocation+'withCollapse.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if "#pragma omp for collapse" in error:
        return error
    else:
        return "success"


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
        return incrementAndRun(numofLoops+1)

    else:
        return numofLoops-1


def collapseAnnotator(filePath,loopStartLine,compilerOptions=''):
    global compilerOptins
    global  fileLocation

    compilerOptins = compilerOptions
    fileName     = "" + filePath.rsplit('/', 1)[1]
    fileLocation = filePath.replace(fileName, "")
    copyFile(fileName)
    addCollapes(loopStartLine)
    results = runCode()
    if(results=="success"):
        print incrementAndRun(2)
        os.remove(fileLocation+"withCollapse.c")
