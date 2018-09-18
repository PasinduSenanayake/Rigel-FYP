from Identifier.nestedLoopChecker import nestedloopAnalysis
from loopAnalyzer import loopAnalysis
from summaryIdentifier.initilizerOmpp import getSummary
from systemIdentifier.systemIdentifier import __systemInformationIdentifier
from nonarchiFeatureFetcherExecuter import gpuAnalzyer
#from vectorFeatureFetcherExecuter import vecAnalzyer
import dbManager,logger
import json
import threading


response = {
    "returncode":0,
    "error":"",
    "content":{}
    }

def selectOptimizableLoopSections(optimizableLoops):
    selectedLoops =[]
    for loopSection in optimizableLoops:
        if(float(optimizableLoops[loopSection]['overheadPrecentage'])> 0.0):
            selectedSection = {
            'fileName':"",
            'identifier':loopSection,
            'startLine': optimizableLoops[loopSection]['startLine'],
            'endLine':optimizableLoops[loopSection]['endLine'],
            'executionTime':optimizableLoops[loopSection]['sectionTime']
            }
            selectedLoops.append(selectedSection)
    return selectedLoops

def identify(extractor,directory):
    global response
    # try:
    logger.loggerInfo("System Information Fetcher Initiated")
    responseObj = __systemInformationIdentifier()
    if(responseObj['returncode']==1):
        dbManager.write('systemData',responseObj['content'])
        logger.loggerSuccess("System Information Fetcher completed successfully")
    else:
        logger.loggerError("System Information Fetcher Failed")
        print "System Information Fetcher Failed. Optimization process terminated."
        exit()
    logger.loggerInfo("Run time arguments fetcher Initiated")
    with open(directory+'/run.json') as runArgumentFile:
        dataArguments = json.load(runArgumentFile)
    if not (dataArguments['runTimeArguments'] == None):
        dbManager.write('runTimeArguments',str(dataArguments['runTimeArguments']))
    else:
        logger.loggerError("Run time arguments fetcher Failed. Optimization process terminated.")
        print "Run time arguments fetcher Failed. Optimization process terminated."
        exit()

    logger.loggerSuccess("Run time arguments fetcher completed successfully")
    logger.loggerInfo("Profile Summarization Initiated")
    summarizedReport = getSummary(directory,dbManager.read('runTimeArguments'))
    if summarizedReport['returncode'] == 1:
        logger.loggerSuccess("Profile Summarization completed successfully")
        loopSections = selectOptimizableLoopSections(summarizedReport['content'])
        if (len(loopSections)>0):
            isGpu = True
            isVector = True
            if not (responseObj['content']['gpuinfo'] == ""): #check Gpu Info
                logger.loggerInfo("Feature Extraction for GPU Initiated")
                gpuThread = threading.Thread(target=gpuAnalzyer,args=(extractor,directory,loopSections,))
                gpuThread.start()
            else:
                isGpu = False
                logger.loggerInfo("No GPU found. GPU offloading will be skipped")
            if(True): #check Vectorization optimizations
                logger.loggerInfo("Available Vector Instructions")
                #display what Instructions available
                logger.loggerInfo("Feature Extraction for Vectorization Initiated")
                # vectorThread = threading.Thread(target=vecAnalzyer,args=(extractor,directory,loopSections,))
                # vectorThread.start()
                #vecAnalzyer(extractor,directory)
            else:
                isVector = False
                logger.loggerInfo("No Vector Instructions were found. Skip Vector optimizations")

            if (isGpu):
                if (isVector):
                    gpuThread.join()
                    #vectorThread.join()
                else:
                    gpuThread.join()
            else:
                if (isVector):
                    ankjdasda = 10
                    #vectorThread.join()
                else:
                    logger.loggerInfo("No hardware support is captured for optimizations. Optimization process terminated.")
                    print "No hardware support is captured for optimizations. Optimization process terminated."
                    exit()

        else:
            logger.loggerInfo("No significant loops available for optimization. Optimization process terminated.")
            print "No significant loops available for optimization. Optimization process terminated."
            exit()
    else:
        logger.loggerError("Profile Summarization Failed. Optimization process terminated.")
        print "Profile Summarization Failed. Optimization process terminated."
        exit()

    # except Exception as e:
    #     print e
    #     response['error'] = e
    #     response['content'] = {}
    #     response['returncode'] = 1
    return response


def trigger1(filePath,compTimeArguments,runTimeArguments):
    try:
        responseObj = nestedloopAnalysis(filePath,compTimeArguments,runTimeArguments)
        if (responseObj['returncode'] == 1):
            response['error'] = ""
            response['content'] = responseObj['content']
            response['returncode'] = 1
    except Exception as e:
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
    return response
