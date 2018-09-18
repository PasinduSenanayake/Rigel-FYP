# json file containing eligible loops
# for now assume all the incoming loops are eligible for offloading
import json
import os
import math
import re,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../../Identifier/systemIdentifier")
from systemIdentifier import __systemInformationIdentifier

""" offloadChecker compose required pragma for loop structures which are eligible for GPU execution
  NOTE: getting input details from clang verbose not implemented
        getting input for iteration space not implemented
        ThreadsPerTeam is calculated which have highest Occupancy and least number of threads
        for not-colllapsible loops split and parallel method is used

  """

TARGET_PRAGMA_COLLAPSE = "#pragma omp target teams num_teams($teams) thread_limit($threads)" \
                         "#pragma omp distribute parallel for collapse($depth) schedule(static,1)"

TARGET_PRAGMA_SPLIT = "#pragma omp target teams num_teams($teams) thread_limit($threads)" \
                      "#pragma omp distribute parallel for schedule(static,1)"

loopOrder = {}
loopMetaData = {}
config = {}
targetPragmaDic = {}
threadsPerWarp = 0
GPUData_File = str(os.path.dirname(
    (os.path.dirname(os.path.realpath(__file__))))) + os.sep + "../Identifier/systemIdentifier/SystemDependencies" + os.sep + "GPUData.json"


def __ceil(a, b):
    c = a / float(b)
    return math.ceil(c) * b


def __floor(a, b):
    c = a / float(b)
    return math.floor(c) * b

#change here
input = {
    "registersPerThread": 42,  # should come from information Json
    "sharedMemoryPerBlock": 932
}

def readGPUData(computeCapability):
    with open(GPUData_File, 'r') as gpuDataFile:
        data = json.load(gpuDataFile)
        global config
        global threadsPerWarp

        config = data[computeCapability]    #change here
        threadsPerWarp = config['threadsPerWarp']


def occupancyCalculator():
    maxThreadBlockSize = config['maxThreadBlockSize'] + 1
    occupancyDic = {}

    for x in range(threadsPerWarp, maxThreadBlockSize, threadsPerWarp):
        warpsPerBlock = math.ceil(x / config['threadsPerWarp'])  # if threadsPerBlock > threadsPerWarp

        if config['allocationGranularity'] == 'block':
            registersPerBlock = __ceil(
                __ceil(warpsPerBlock, config['warpAllocationGranularity']) * input['registersPerThread'] * config[
                    'threadsPerWarp'],
                config['registerAllocationUnitSize'])
            multiprocessorRegisters = config['registerFileSize']  # total number of registers per SM

        else:
            registersPerWarp = __ceil(input['registersPerThread'] * config['threadsPerWarp'],
                                      config['registerAllocationUnitSize'])
            registersPerBlock = registersPerWarp * warpsPerBlock  # 12288

            # warpAllocationGranularity means number of warps being allocated at a time
            # maximum number of register for the maximum number of accommodatable warps 61440
            multiprocessorRegisters = __floor(config['registerFileSize'] / registersPerWarp,
                                              config['warpAllocationGranularity']) * registersPerWarp

        sharedMemoryPerBlock = __ceil(input['sharedMemoryPerBlock'], config['sharedMemoryAllocationUnitSize'])
        # maximum amount of shared memory being allocated for a block

        threadBlocksPerMultiprocessorLimitedByWarpsOrBlocksPerMultiprocessor = min(
            config['threadBlocksPerMultiprocessor'], math.floor(config['warpsPerMultiprocessor'] / warpsPerBlock))
        # 16 block max but 8 limited by warps
        # calculate maximum number of blocks blocks that can accommodate the SM

        if input['registersPerThread'] > config['maxRegistersPerThread']:
            threadBlocksPerMultiprocessorLimitedByRegistersPerMultiprocessor = 0
        else:
            if input['registersPerThread'] > 0:
                threadBlocksPerMultiprocessorLimitedByRegistersPerMultiprocessor = math.floor(
                    multiprocessorRegisters / registersPerBlock)
                # determines number of blocks that can use existing registers 50
            else:
                threadBlocksPerMultiprocessorLimitedByRegistersPerMultiprocessor = config[
                    'threadBlocksPerMultiprocessor']  # when number of blocks can not be calculated  16

        if input['sharedMemoryPerBlock'] > 0:
            threadBlocksPerMultiprocessorLimitedBySharedMemoryPerMultiprocessor = math.floor(
                config['sharedMemoryPerMultiprocessor'] / sharedMemoryPerBlock)
            # calculates number of blocks depending on shared memory
        else:
            threadBlocksPerMultiprocessorLimitedBySharedMemoryPerMultiprocessor = config[
                'threadBlocksPerMultiprocessor']
            # else assign the maximum possible number of blocks

        # takes the minimum factor which can allocate resources evenly
        activeThreadBlocksPerMultiprocessor = min(
            threadBlocksPerMultiprocessorLimitedByWarpsOrBlocksPerMultiprocessor,  # 8
            threadBlocksPerMultiprocessorLimitedByRegistersPerMultiprocessor,  # 5
            threadBlocksPerMultiprocessorLimitedBySharedMemoryPerMultiprocessor  # 192
        )

        activeWarpsPerMultiprocessor = activeThreadBlocksPerMultiprocessor * warpsPerBlock

        occupancyOfMultiprocessor = activeWarpsPerMultiprocessor / config['warpsPerMultiprocessor']

        if occupancyOfMultiprocessor in occupancyDic:
            occupancyDic[occupancyOfMultiprocessor].append(x)
        else:
            list_ = [x]
            occupancyDic[occupancyOfMultiprocessor] = list_

    maxOccupancy = max(list(occupancyDic))
    return occupancyDic[maxOccupancy]


# find collapsible depth
def colllapsibleDepth(key, value, loopMetaData):
    if len(value) == 1:
        if (loopMetaData[key]['loopMeta']['collapse'][1]):
            if isinstance(value[0], dict):
                for key1, value1 in value[0].iteritems():
                    return 1 + colllapsibleDepth(key1, value1, loopMetaData)
            else:
                return 2
        else:
            return 1
    else:
        return 1


def calculateTeams(threadsPerTeam, iterationSpace):
    remainder = iterationSpace % threadsPerTeam
    if (remainder) > 0:  # not a multiple of 32
        iterationSpace = threadsPerTeam - remainder + iterationSpace
    teams = iterationSpace / threadsPerTeam
    return teams


def pragmaGenerator(depth, threadsPerTeam, teams):
    if (depth == 1):  # not collapsible
        rep = {"$teams": str(teams), "$threads":str(threadsPerTeam)}  # define desired replacements here
        string = TARGET_PRAGMA_SPLIT

    else:
        rep = {"$teams": str(teams), "$threads": str(threadsPerTeam),"$depth": str(depth)}  # define desired replacements here
        string = TARGET_PRAGMA_COLLAPSE

    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], string)


# collapsible
# number of teams
# number of threads
def loadLoopData(looporder, loopmetadata):
    loopOrder = looporder
    loopMetaData = loopmetadata
    global targetPragmaDic
    readGPUData()
    print loopOrder
    print loopMetaData
    for key, value in loopOrder.iteritems():
        iterations = 4096*4096
        depth = colllapsibleDepth(key, value, loopMetaData)
        threadsPerTeam = occupancyCalculator()
        teams = calculateTeams(threadsPerTeam, iterations)
        outputPragma = pragmaGenerator(depth, threadsPerTeam, teams)
        targetPragmaDic[key] = outputPragma
    print targetPragmaDic

# for now we have considered all the loop levels as collapsible
# in case of vectorization we can reduce number of loop levels by 1 to remove inner most loop from collapsing
# in case number of threads are greater than iteration space
# hint from more teams with less threads

def occupancyCalculation(registersPerThread,sharedMemoryPerBlock):
    global input
    input["registersPerThread"] = float(registersPerThread)
    input["sharedMemoryPerBlock"] = float(sharedMemoryPerBlock)
    responseObj = __systemInformationIdentifier()
    if responseObj['returncode'] == 1:
            gpuInfo = responseObj['content']['gpuinfo']
            nvidiaGPUList = [key for key in gpuInfo if "NVIDIA" in key]
            computeCapability = gpuInfo[nvidiaGPUList[0]]['compute_capability']
            readGPUData(computeCapability)
            threadsPerTeamList = occupancyCalculator()
            return threadsPerTeamList
