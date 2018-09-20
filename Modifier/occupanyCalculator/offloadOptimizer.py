#Assume results are passed with code line segment and suitability
#for each loop segment suitable need to calulate occupancy
#by compiling and determining registers and shared memory usage

import os,sys
import json
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/../../Logger")
import logger
import shutil
import subprocess
from offloadChecker import  occupancyCalculation
from GpuTarget import mapTargetData
from collapsibleFinder import  collapseAnnotator


TARGET_PRAGMA_INITIALIZE = "#pragma omp target teams\n" \
                            "#pragma omp distribute parallel for schedule(static,1)"


TARGET_PRAGMA_COLLAPSE = "#pragma omp target teams thread_limit($threads)\n" \
                         "#pragma omp distribute parallel for collapse($depth) schedule(static,1)"

TARGET_PRAGMA_SPLIT = "#pragma omp target teams  thread_limit($threads)\n" \
                      "#pragma omp distribute parallel for schedule(static,1)"

CLANG_OFFLOAD = "CC = clang -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda -v "

CLANG = "cc=clang"
MAKE = "make"
MAKEFILE = "Makefile"
makePath = ''
modifierOffloaderFilePath = "/../modifierSandbox/OffloaderSandbox/Sandbox"

if(os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/../../subCommandConf.json")):
    with open(os.path.dirname(os.path.realpath(__file__))+"/../../subCommandConf.json") as f:
        commandJson = json.load(f)

result = {
    'code':0,
    'content':[],
    'error':'',
    'successMessage':''
    }

input = {
    "registersPerThread":0,  # should come from information Json
    "sharedMemoryPerBlock": 0
}

loopList = [[22,32]]
extractorPassObject = {'index': 0, 'pragma': ''}
extractorPragmaList = []

def moveSandbox():
    global result

    print str(os.path.dirname(os.path.realpath(__file__)))

    logger.loggerInfo("Source Code Annotation Command Initiated")
    path = os.path.dirname(os.path.realpath(__file__)) + modifierOffloaderFilePath
    if(os.path.exists(path)):
        shutil.rmtree(os.path.dirname(os.path.realpath(__file__)) + modifierOffloaderFilePath)
    try:
        shutil.copytree(os.path.dirname(os.path.realpath(__file__))+"/../../Sandbox", os.path.dirname(os.path.realpath(__file__)) + modifierOffloaderFilePath)
    except Exception as e:
        logger.loggerError(e)


def readClangVerbose():
    global input
    global makePath
    makefile = commandJson["command"]["nonArchiFeatureFetch"]["makeFile"]
    makefilePath = os.path.dirname(os.path.realpath(__file__)) + modifierOffloaderFilePath + \
                   makefile.split("Sandbox")[1]

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
    makefile = commandJson["command"]["nonArchiFeatureFetch"]["makeFile"]
    makefilePath = os.path.dirname(os.path.realpath(__file__))+ modifierOffloaderFilePath + makefile.split("Sandbox")[1]
    check = True

    with open(makefilePath,'r') as f:
        makeFileContentList = f.readlines()

    makefileContent = ""
    for line in makeFileContentList:
        if check and CLANG in line.lower().replace(" ","").strip():
            makefileContent = makefileContent + CLANG_OFFLOAD
            check = False
        else:
            makefileContent = makefileContent + line

    with open(makefilePath,'w') as f:
        f.write(makefileContent)


def __runOptimizerStandalone():
    global loopList
    global makePath
    global extractorPragmaList

    annotatedFile = commandJson["command"]["nonArchiFeatureFetch"]["annotatedFile"]
    offloadFilePath = os.path.dirname(os.path.realpath(__file__)) + modifierOffloaderFilePath + annotatedFile.split("Sandbox")[1]
    loopStartList = []

    for x in loopList:
        y = x[0]
        loopStartList.append(y)

    loopList.sort() #sorts list of loops respect to their starting index

    with open(offloadFilePath, "r") as f:
        contentList = f.readlines()

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
        TARGET_MAP_PRAGMA =  mapTargetData(offloadFilePath, x, end[0])

        collapsibleDepth  = collapseAnnotator(offloadFilePath,x)

        if collapsibleDepth > 1:
            TARGET_PRAGMA = TARGET_PRAGMA_COLLAPSE.replace('$depth', collapsibleDepth)
        else:
            TARGET_PRAGMA = TARGET_PRAGMA_SPLIT


        OMP_GET_STIME = 'double omp_getwtime1,omp_getwtime2;\n' \
                        'omp_getwtime1 = omp_get_wtime();\n'
        OMP_GET_ETIME = 'omp_getwtime2 = omp_get_wtime();\n' \
                        'printf("GPU Runtime:%0.6lf", omp_getwtime2 - omp_getwtime1);\n' \
                        'exit(0)'

        FINALIZED_PRGAMA = OMP_GET_STIME + TARGET_MAP_PRAGMA + '\n' + TARGET_PRAGMA

        timeList = []
        for threads in threadsPerTeamList:
            FINALIZED_PRGAMA = FINALIZED_PRGAMA.replace('$threads',str(threads))
            lineNumber = 0
            content = '#include <omp.h>\n'
            for line in contentList:
                if x == lineNumber + 1:
                    content = content + FINALIZED_PRGAMA
                elif lineNumber == end[0]:
                    content = content + OMP_GET_ETIME
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

        print val,' ',idx
        print threadsPerTeamList[idx]
    print extractorPragmaList


def runOffloadOptimizer():
    moveSandbox()
    __runOptimizerStandalone()

if __name__ == "__main__":
    logger.createLog()
    logger.loggerInfo("Offload Optimizer initiated")
    moveSandbox()
    __runOptimizerStandalone()
