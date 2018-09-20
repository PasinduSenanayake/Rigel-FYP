#Assume results are passed with code line segment and suitability
#for each loop segment suitable need to calulate occupancy
#by compiling and determining registers and shared memory usage

import os,sys
import json
import logger, dbManager
import shutil
import subprocess
from offloadChecker import occupancyCalculation
from GpuTarget import mapTargetData
from collapsibleFinder import collapseAnnotator


TARGET_PRAGMA_INITIALIZE = "#pragma omp target teams\n" \
                            "#pragma omp distribute parallel for schedule(static,1)\n"


TARGET_PRAGMA_COLLAPSE = "#pragma omp target teams thread_limit($threads)\n" \
                         "#pragma omp distribute parallel for collapse($depth) schedule(static,1)\n"

TARGET_PRAGMA_SPLIT = "#pragma omp target teams  thread_limit($threads)\n" \
                      "#pragma omp distribute parallel for schedule(static,1)\n"

CLANG_OFFLOAD = "CC = clang -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda -v "

CLANG = "[compiler]"
MAKE = "make"
MAKEFILE = "Makefile"
makePath = ''
movePath = os.path.dirname(os.path.realpath(__file__)) + "/../modifierSandbox/OffloaderSandbox/Sandbox"

result = {
    'code':0,
    'content': [],
    'error': '',
    'successMessage': ''
    }

input = {
    "registersPerThread": 0,  # should come from information Json
    "sharedMemoryPerBlock": 0
}

loopList = [[22, 32]]
extractorPassObject = {'index': 0, 'pragma': ''}
extractorPragmaList = []
folderPath_ = ''
folderName = ''

def moveSandbox():
    global result
    global folderName

    originalPath  = folderPath_ + '/_profiling/Sandbox'
    folderName = folderPath_.split('Sandbox')[1].replace('/','')

    if(os.path.exists(movePath)):
        shutil.rmtree(movePath)
    try:
         shutil.copytree(originalPath, movePath+'/'+folderName)
         logger.loggerInfo('Moving to OffloaderSandbox')

    except Exception as e:
         logger.loggerError(e)
         result['code'] = 1
         result['content']= []
         result['error']= e
         result['successMessage'] = ''
         logger.loggerError("Moving to OffloaderSandbox failed")



def readClangVerbose():
    global input
    global makePath
    makefilePath = movePath + '/' + folderName + '/Makefile'

    makePath ='cd ' + makefilePath.replace('/'+MAKEFILE, '') + '  &&  ' + MAKE

    p = subprocess.Popen(makePath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    (output, err) = p.communicate()  # to check for errors
    verbose = err.splitlines()
    nvlinkInfo = []
    for s in verbose:
        if "nvlink info" in s:
            nvlinkInfo.append(s)
    if len(nvlinkInfo) == 0:
        print "Error compiling Offload Optimizer make"
    else:
        occupancydata  =  nvlinkInfo[2].split(",")
        occupancydata[0] = occupancydata[0].split(":")[1]
        input['registersPerThread'] = occupancydata[0].split(" ")[2]
        input['sharedMemoryPerBlock'] = occupancydata[2].split(" ")[1]


def changeMakeFile():
    makefilePath = movePath + '/' + folderName + '/' + MAKEFILE
    check = True

    with open(makefilePath,'r') as f:
        makeFileContentList = f.readlines()

    makefileContent = ""
    for line in makeFileContentList:
        if CLANG in line:
            makefileContent = makefileContent + CLANG_OFFLOAD
        elif '[targetObject]' in line :
            makefileContent = makefileContent + line.replace('[targetObject]', 'runnable')
        elif '.c' in line:
            makefileContent = makefileContent + line.replace('.c','_serial.c')
        else:
            makefileContent = makefileContent + line

    with open(makefilePath,'w') as f:
        f.write(makefileContent)


def __runOptimizerStandalone(extractor):
    global loopList
    global makePath
    global extractorPragmaList

    loopSections = dbManager.read('loopSections')
    offloadFilePath = movePath + '/' + folderName + '/' + loopSections[0]['fileName'].replace('.c', '_serial.c')
    loopStartList = []
    loopEndList = []

    for x in loopSections:
        y = int(x['serialStartLine'])
        loopStartList.append(y)
        loopEndList.append(int(x['serialEndLine']))

    loopList.sort() #sorts list of loops respect to their starting index
    loopEndList.sort()

    with open(offloadFilePath, "r") as f:
        contentList = f.readlines()

    index = 0
    for x in loopStartList:
        content = ""
        lineNumber = 0
        for line in contentList:
            if x == lineNumber + 1:
                content = content + TARGET_PRAGMA_INITIALIZE
            else:
                content = content + line
            lineNumber = lineNumber + 1
        with open(offloadFilePath,'w') as f:
            f.write(content)
        changeMakeFile()
        readClangVerbose()
        threadsPerTeamList = occupancyCalculation(input['registersPerThread'], input['sharedMemoryPerBlock'])
        end =[ y[1] for y in loopList if y[0]==x]
        TARGET_MAP_PRAGMA = mapTargetData(offloadFilePath, x, loopEndList[index])


        collapsibleDepth  = collapseAnnotator(offloadFilePath,x)

        if collapsibleDepth > 1:
            TARGET_PRAGMA = TARGET_PRAGMA_COLLAPSE.replace('$depth', collapsibleDepth)
        else:
            TARGET_PRAGMA = TARGET_PRAGMA_SPLIT


        OMP_GET_STIME = 'double omp_getwtime1,omp_getwtime2;\n' \
                        'omp_getwtime1 = omp_get_wtime();\n'
        OMP_GET_ETIME = 'omp_getwtime2 = omp_get_wtime();\n' \
                        'printf("GPU Runtime:%0.6lf", omp_getwtime2 - omp_getwtime1);\n' \
                        'exit(0);\n'

        FINALIZED_PRGAMA = OMP_GET_STIME + TARGET_MAP_PRAGMA + '\n' + TARGET_PRAGMA

        timeList = []
        for threads in threadsPerTeamList:
            FINALIZED_PRGAMA = FINALIZED_PRGAMA.replace('$threads',str(threads))
            lineNumber = 1
            content = '#include <omp.h>\n'
            for line in contentList:
                if x == lineNumber :
                    content = content + line + FINALIZED_PRGAMA
                elif lineNumber == loopEndList[index]:
                    content = content + OMP_GET_ETIME + line
                else:
                    content = content + line
                lineNumber = lineNumber + 1

            #writing to the new file
            with open(offloadFilePath,'w') as f:
                 f.write(content)

            runnablePath = makePath + '&& ./runnable '
            p = subprocess.Popen(runnablePath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE)
            (output, err) = p.communicate()  # to check for errors
            runnableList = output.splitlines()
            print output
            for s in runnableList:
                if "GPU Runtime:" in s:
                    timeList.append(float(s.split(":")[1].strip()))
                    break

        val, idx = min((val, idx) for (idx, val) in enumerate(timeList))

        if collapsibleDepth > 1:
            TARGET_PRAGMA = TARGET_PRAGMA_COLLAPSE.replace('$depth', collapsibleDepth)
        else:
            TARGET_PRAGMA = TARGET_PRAGMA_SPLIT

        EXTRACTOR_PRAGMA = TARGET_MAP_PRAGMA + '\n' + TARGET_PRAGMA.replace('$threads', str(threadsPerTeamList[idx]))

        extractorPassObject['index'] = x
        extractorPassObject['pragma'] = EXTRACTOR_PRAGMA
        extractorPragmaList.append(extractorPassObject)
        extractor

        index = index + 1
        print val,' ',idx
        print threadsPerTeamList[idx]
    print extractorPragmaList


def runOffloadOptimizer( extractor , folderPath):
    global folderPath_
    folderPath_ = folderPath
    logger.loggerInfo("GPU Offloder Optimizer initiated")
    moveSandbox()
    __runOptimizerStandalone(extractor)

if __name__ == "__main__":
    logger.createLog()
    logger.loggerInfo("Offload Optimizer initiated")
    moveSandbox()
    __runOptimizerStandalone()
