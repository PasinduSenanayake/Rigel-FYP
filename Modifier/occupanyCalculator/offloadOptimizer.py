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
from Extractor.SourceCode import SourceCode
from Extractor.Extractor import Extractor



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
         shutil.copytree(originalPath, movePath + '/' + folderName)
         logger.loggerSuccess('Moved to OffloaderSandbox for offload optimization')
         result['code'] = 0

    except Exception as e:
         logger.loggerError(e)
         result['code'] = 1
         result['content']= []
         result['error']= e
         result['successMessage'] = ''
         logger.loggerError("Moving to OffloaderSandbox failed")

    return result

def readClangVerbose():
    global input
    global makePath
    global result
    makefilePath = movePath + '/' + folderName + '/Makefile'

    makePath ='cd ' + makefilePath.replace('/' + MAKEFILE, '') + '  &&  ' + MAKE

    p = subprocess.Popen(makePath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    (output, err) = p.communicate()  # to check for errors
    verbose = err.splitlines()
    nvlinkInfo = []
    for s in verbose:
        if "nvlink info" in s:
            nvlinkInfo.append(s)
    if len(nvlinkInfo) == 0:
        logger.loggerError('Offload Optimizer reading clang verbose failed ')
        result['code'] = 1
        result['content'] = []
        result['error'] = err
        result['successMessage'] = ''

    else:
        occupancydata  =  nvlinkInfo[2].split(",")
        occupancydata[0] = occupancydata[0].split(":")[1]
        input['registersPerThread'] = occupancydata[0].split(" ")[2]
        input['sharedMemoryPerBlock'] = occupancydata[2].split(" ")[1]
        logger.loggerSuccess('Offload Optimizer reading clang verbose')
        result['code'] = 0
    return result


def changeMakeFile():
    global result
    makefilePath = movePath + '/' + folderName + '/' + MAKEFILE

    try:
        with open(makefilePath,'r') as f:
            makeFileContentList = f.readlines()
            makefileContent = ""
        for line in makeFileContentList:
            if CLANG in line:
                makefileContent = makefileContent + CLANG_OFFLOAD
            elif '[targetObject]' in line:
                makefileContent = makefileContent + line.replace('[targetObject]', 'runnable')
            elif '.c' in line:
                makefileContent = makefileContent + line.replace('.c', '_serial.c')
            else:
                makefileContent = makefileContent + line

        with open(makefilePath, 'w') as f:
            f.write(makefileContent)

        logger.loggerSuccess('OffloadOptimizer successfully created makefile')
        result['code'] = 0
    except Exception as e:
        logger.loggerError(e)
        result['code'] = 1
        result['content'] = []
        result['error'] = e
        result['successMessage'] = ''
        logger.loggerError("OffloadOptimizer make file creation failed")
    return result


def __runOptimizerStandalone(extractor):
    global makePath
    fileName = ''
    sourceObjList = {}
    loopSections = dbManager.read('loopSections')
    isGPU = False

    for loop in loopSections:
        if loop['optimizeMethod'] == 'GPU':
            isGPU = True
            break

    if isGPU:
        logger.loggerInfo("GPU Offloader Optimizer initiated")
        summarySections = dbManager.read('summaryLoops')
        status = changeMakeFile()

        with open(movePath + '/' + folderName + '/'+'run.json') as inputfile:
            runJson = json.load(inputfile)
            runtimeArg = runJson['runTimeArguments']

        if status['code'] == 0:
            for loopSection in loopSections:
                if loopSection['optimizeMethod'] =='GPU':
                    if fileName != loopSection['fileName']:
                        fileName = loopSection['fileName']
                        if fileName in sourceObjList.keys():
                            sourceObj = sourceObjList[fileName]
                        else:
                            sourceObj = extractor.getSource(folderPath_ + '/' + fileName)
                            sourceObjList[fileName] = sourceObj

                        offloadFolderPath = movePath + '/' + folderName + '/' + fileName.replace('.c', '_serial.c')
                        with open(offloadFolderPath, "r") as f:
                            contentList = f.readlines()

                    startIndex = int(loopSection['serialStartLine'])
                    endIndex   = int(loopSection['serialEndLine'])

                    collapsibleDepth = collapseAnnotator(offloadFolderPath, startIndex, contentList)
                    content = ""
                    lineNumber = 0
                    for line in contentList:
                        if startIndex == lineNumber + 1:
                            content = content + line + TARGET_PRAGMA_INITIALIZE
                        else:
                            content = content + line
                        lineNumber = lineNumber + 1

                    with open(offloadFolderPath, 'w') as f:
                        f.write(content)

                    status = readClangVerbose()
                    if status['code'] == 0:
                        threadsPerTeamList = occupancyCalculation(input['registersPerThread'], input['sharedMemoryPerBlock'])
                        TARGET_MAP_PRAGMA = mapTargetData(offloadFolderPath, startIndex, endIndex)

                        print collapsibleDepth

                        if collapsibleDepth > 1:
                            TARGET_PRAGMA = TARGET_PRAGMA_COLLAPSE.replace('$depth', str(collapsibleDepth))
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
                            content = '//GPU optimzation\n'
                            for line in contentList:
                                if startIndex == lineNumber :
                                    content = content + line + FINALIZED_PRGAMA
                                elif lineNumber == endIndex:
                                    content = content + OMP_GET_ETIME + line
                                else:
                                    content = content + line
                                lineNumber = lineNumber + 1

                            #writing to the new file
                            with open(offloadFolderPath,'w') as f:
                                 f.write(content)

                            runnablePath = makePath + '&& ./runnable ' + runtimeArg + ' '
                            p = subprocess.Popen(runnablePath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                  stdin=subprocess.PIPE)
                            (output, err) = p.communicate()  # to check for errors
                            runnableList  = output.splitlines()
                            clangError = True
                            for s in runnableList:
                                if "GPU Runtime:" in s:
                                    timeList.append(float(s.split(":")[1].strip()))
                                    clangError = False
                                    break
                            if clangError:
                                logger.loggerError('Optimized code execution failure. check Clang compiler')

                        print(timeList)
                        val, idx = min((val, idx) for (idx, val) in enumerate(timeList))
                        optimizationTime = sum(timeList)
                        dbManager.write('GPU_OptTime', str(optimizationTime))

                        if collapsibleDepth > 1:
                            TARGET_PRAGMA = TARGET_PRAGMA_COLLAPSE.replace('$depth', str(collapsibleDepth))
                        else:
                            TARGET_PRAGMA = TARGET_PRAGMA_SPLIT

                        EXTRACTOR_PRAGMA = TARGET_MAP_PRAGMA + '\n' + TARGET_PRAGMA.replace('$threads', str(threadsPerTeamList[idx]))
                        print EXTRACTOR_PRAGMA
                        sourceObj.offload(loopSection['startLine'],EXTRACTOR_PRAGMA)
                        sourceObj.writeToFile(folderPath_+'/'+fileName)
                        for summaryLoop in summarySections:
                            if summaryLoop['startLine'] == loopSection['startLine']:
                                summaryLoop['optimizedTime'] = str(val)



            else:
                dbManager.overWrite('summaryLoops',summarySections )
                if (os.path.exists(movePath)):
                    shutil.rmtree(movePath)
    else:
        logger.loggerInfo('GPU Optimizable loops not found')


def runOffloadOptimizer( extractor, folderPath):
    global folderPath_
    folderPath_ = folderPath

    status = moveSandbox()
    if status['code'] == 0:
        __runOptimizerStandalone(extractor)
    else:
        return result

if __name__ == "__main__":
    logger.createLog()
    logger.loggerInfo("Offload Optimizer initiated")
    moveSandbox()
    __runOptimizerStandalone()
