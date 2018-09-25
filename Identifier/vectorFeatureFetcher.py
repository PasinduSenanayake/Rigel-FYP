import dbManager,logger,os,shutil
import hashlib,dbManager
import gc
import glob
import pandas as pd

from Identifier.identifierSandbox.vectorDataFetcher import vtuneProfiler
from nonarchiFeatureFetcher import hotspotsProfiler

def featureExtractionExecutor(extractor,directory,loopSections,fileNames):
    with open(directory + "/_vector_profiling/Sandbox/Makefile", 'r') as file :
        filedata = file.read()
        filedata = filedata.replace('.c', '_serial.c')
    with open(directory + "/_vector_profiling/Sandbox/Makefile", 'w') as file:
        file.write(filedata)
    for fileName in fileNames:
        filePath = directory + "/" + fileName
        fileFeaturePath = directory + "/_vector_profiling/Sandbox/" + fileName
        fileTempPath = filePath.replace("_serial.c",".c")
        sourceObj = extractor.getSource(fileTempPath)
        serialSections = []
        parallelSections = []
        for item in  sourceObj.serialParallelOuterLoopMap():
            for subItem in sourceObj.serialParallelOuterLoopMap()[item]:
                if item == "serial":
                    serialSections.append(str(subItem.lineNumber)+":"+str(subItem.endLineNumber))
                else:
                    parallelSections.append(str(subItem.lineNumber)+":"+str(subItem.endLineNumber))

        for index,element in enumerate(serialSections):
            parallelStartLine = parallelSections[index].split(":")[0]
            parallelEndLine = parallelSections[index].split(":")[1]
            isIn = 'None'
            for data in loopSections:
                #Can have the file Name restrictions if required.
                if(data['startLine'] == str(int(parallelStartLine)-1) ):
                    if (data['endLine'] == parallelEndLine ):
                        if(data['optimiazability']):
                            isIn = 'proceed'
                            break
                        else:
                            isIn = 'notSig'

            if (isIn=='proceed'):
                sequentialStartLine = int(element.split(":")[0]) - 1
                sequentialEndLine =int(element.split(":")[1]) + 1
                fileName = fileName.replace("_serial.c",".c")
                codeName = fileName+":p["+str(data['startLine'])+"-"+str(data['endLine'])+"]"
                folderPath = directory + "/_vector_profiling/Sandbox"
                loopSegments = [[sequentialStartLine,sequentialEndLine]]
                logger.loggerInfo("Vector Feature Extraction Process Initiated for section "+parallelStartLine+":"+parallelEndLine)
                vtuneProfiler(codeName,fileFeaturePath.replace('.c','_serial.c'),fileFeaturePath.replace('.c','_serial.c'),folderPath+"/Makefile","",dbManager.read('runTimeArguments'),loopSegments,directory+"/_vector_profiling",False)
                gc.collect()

                logger.loggerSuccess("Vector Feature Extraction Process completed for section "+parallelStartLine+":"+parallelEndLine)
            elif(isIn=='notSig'):
                logger.loggerInfo("Section "+parallelStartLine+":"+parallelEndLine+" is skipped due to low overhead")
            else:
                logger.loggerInfo("Section "+parallelStartLine+":"+parallelEndLine+" is not a parallelable region. Skipped")



def vecAnalzyer(extractor,directory,loopSections):
    fileData =[]
    logger.loggerInfo("Creating sequential files initiated")
    directoryName = directory.split("/")[-1]
    workingDir = directory + "/_vector_profiling/Sandbox"
    if os.path.exists(workingDir):
        shutil.rmtree(workingDir)
    os.makedirs(workingDir)
    filenames = []
    for fileModify in os.listdir(directory):
        filePath = directory + "/" + fileModify
        if os.path.isfile(filePath):
            if fileModify.endswith(".c"):
                filenames.append(fileModify.split('/')[-1])
                sourceObj = extractor.getSource(filePath)
                sourceObj.writeToFile(workingDir + "/" + fileModify, sourceObj.root)
                sourceObj.writeToFile(workingDir + "/" + fileModify[:-2] + "_serial.c", sourceObj.serialroot)
            else:
                shutil.copyfile(filePath, workingDir + "/" + fileModify)

    featureExtractionExecutor(extractor,directory,loopSections,filenames)
    # print('fkdsjfksdjfsldfldlsf')
    preparefeatureData(directory+"/_vector_profiling")
    logger.loggerSuccess("Sequential file creation completed")

def extract(string, start='[', stop=']'):
    return string[string.index(start) + 1:string.index(stop)]

def preparefeatureData(location):
    if (os.path.isfile(location+'/out.csv')):
        os.remove(location+'/out.csv')
    dfList = []
    for fname in glob.glob(location+"/*.csv"):
        df = pd.read_csv(fname)
        headerlist = list(df)
        i = 0
        for i in range(len(headerlist)):
            headerlist[i] = headerlist[i].replace('Hardware Event Count:','')
            if headerlist[i] == 'Function':
                headerlist[i] = 'Function / Call Stack'
            # print(header)
        # print(headerlist)
        df.columns = headerlist

        featureSet1 = [ 'Function / Call Stack','CPU_CLK_UNHALTED.THREAD',
                       'CPU_CLK_UNHALTED.REF_TSC', 'INST_RETIRED.ANY', 'INST_RETIRED.PREC_DIST',
                       'BR_MISP_RETIRED.ALL_BRANCHES_PS', 'CYCLE_ACTIVITY.STALLS_MEM_ANY',
                       'FRONTEND_RETIRED.DSB_MISS_PS']
        featureSet2 = ['FRONTEND_RETIRED.LATENCY_GE_16_PS', 'FRONTEND_RETIRED.LATENCY_GE_2_BUBBLES_GE_1_PS',
                       'MEM_INST_RETIRED.ALL_STORES_PS', 'MEM_INST_RETIRED.SPLIT_LOADS_PS',
                       'MEM_INST_RETIRED.SPLIT_STORES_PS', 'MEM_LOAD_RETIRED.FB_HIT_PS', 'MEM_LOAD_RETIRED.L1_HIT_PS',
                       'MEM_LOAD_RETIRED.L1_MISS_PS', 'MEM_LOAD_RETIRED.L2_HIT_PS', 'MEM_LOAD_RETIRED.L3_HIT_PS']
        featureSet3 = ['MEM_LOAD_RETIRED.L3_MISS_PS', 'ARITH.DIVIDER_ACTIVE', 'BACLEARS.ANY',
                       'CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE', 'CPU_CLK_UNHALTED.REF_XCLK', 'CPU_CLK_UNHALTED.THREAD_P',
                       'CYCLE_ACTIVITY.STALLS_L1D_MISS', 'CYCLE_ACTIVITY.STALLS_L2_MISS',
                       'CYCLE_ACTIVITY.STALLS_L3_MISS', 'DSB2MITE_SWITCHES.PENALTY_CYCLES']
        featureSet4 = ['DTLB_LOAD_MISSES.STLB_HIT', 'DTLB_LOAD_MISSES.WALK_ACTIVE', 'DTLB_STORE_MISSES.STLB_HIT',
                       'EXE_ACTIVITY.1_PORTS_UTIL', 'EXE_ACTIVITY.2_PORTS_UTIL', 'EXE_ACTIVITY.BOUND_ON_STORES',
                       'EXE_ACTIVITY.EXE_BOUND_0_PORTS', 'FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE',
                       'FP_ARITH_INST_RETIRED.SCALAR_SINGLE', 'FP_ASSIST.ANY']
        featureSet5 = ['ICACHE_16B.IFDATA_STALL', 'ICACHE_64B.IFTAG_STALL', 'IDQ.ALL_DSB_CYCLES_4_UOPS',
                       'IDQ.ALL_DSB_CYCLES_ANY_UOPS', 'IDQ.ALL_MITE_CYCLES_4_UOPS', 'IDQ.ALL_MITE_CYCLES_ANY_UOPS',
                       'IDQ.DSB_UOPS', 'IDQ.MITE_UOPS', 'IDQ.MS_SWITCHES', 'IDQ.MS_UOPS']
        featureSet6 = ['IDQ_UOPS_NOT_DELIVERED.CORE', 'IDQ_UOPS_NOT_DELIVERED.CYCLES_0_UOPS_DELIV.CORE',
                       'INT_MISC.CLEAR_RESTEER_CYCLES', 'INT_MISC.RECOVERY_CYCLES', 'L1D_PEND_MISS.FB_FULL:cmask=1',
                       'L1D_PEND_MISS.PENDING', 'L2_RQSTS.RFO_HIT', 'LD_BLOCKS.NO_SR', 'LD_BLOCKS.STORE_FORWARD',
                       'LD_BLOCKS_PARTIAL.ADDRESS_ALIAS']
        featureSet7 = ['MACHINE_CLEARS.COUNT', 'OFFCORE_REQUESTS_BUFFER.SQ_FULL',
                       'OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD:cmask=4',
                       'OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DATA_RD',
                       'OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO', 'RS_EVENTS.EMPTY_CYCLES',
                       'RS_EVENTS.EMPTY_END', 'UOPS_DISPATCHED_PORT.PORT_0', 'UOPS_DISPATCHED_PORT.PORT_1',
                       'UOPS_DISPATCHED_PORT.PORT_2']
        featureSet8 = ['UOPS_DISPATCHED_PORT.PORT_3', 'UOPS_DISPATCHED_PORT.PORT_4', 'UOPS_DISPATCHED_PORT.PORT_5',
                       'UOPS_DISPATCHED_PORT.PORT_6', 'UOPS_DISPATCHED_PORT.PORT_7', 'UOPS_EXECUTED.CORE_CYCLES_GE_1',
                       'UOPS_EXECUTED.CORE_CYCLES_GE_2', 'UOPS_EXECUTED.CORE_CYCLES_GE_3',
                       'UOPS_EXECUTED.CORE_CYCLES_NONE', 'UOPS_EXECUTED.THREAD', 'UOPS_ISSUED.ANY',
                       'UOPS_RETIRED.RETIRE_SLOTS']

        allFeatures = featureSet1 + featureSet2 + featureSet3 + featureSet4 + featureSet5 + featureSet6 + featureSet7 + featureSet8
        df = df[allFeatures]
        # print(df.head)
        df = df.loc[df['Function / Call Stack'] == 'profileHook']
        # print(df.head)
        df['CPI Rate'] = df.apply(lambda row: row['CPU_CLK_UNHALTED.THREAD'] / float( row['INST_RETIRED.ANY']), axis=1)
        # print(fname)
        df.loc[df[ 'Function / Call Stack'] == 'profileHook', 'Function / Call Stack'] = extract(fname)
        dfList.append(df)
        os.remove(fname)
    bigdata = pd.concat(dfList, ignore_index=True)
    print(bigdata)
    bigdata.to_csv(location+'/out.csv')