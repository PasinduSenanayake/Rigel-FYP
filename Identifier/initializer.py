from Identifier.nestedLoopChecker import nestedloopAnalysis
from Identifier.vectorFeatureFetcher import vecAnalzyer
from loopAnalyzer import loopAnalysis
from summaryIdentifier.initilizerOmpp import getSummary
from systemIdentifier.systemIdentifier import __systemInformationIdentifier
from nonarchiFeatureFetcherExecuter import gpuAnalzyer
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
    summaryLoops = []
    for loopSection in optimizableLoops:
        selectedSection = {
        'fileName':optimizableLoops[loopSection]['fileName'],
        'identifier':loopSection,
        'startLine': optimizableLoops[loopSection]['startLine'],
        'endLine':optimizableLoops[loopSection]['endLine'],
        'serialStartLine':0,
        'serialEndLine':0,
        'executionTime':optimizableLoops[loopSection]['sectionTime'],
        'optimiazability':False,
        'optimizeMethod':None
        }
        summarySection = {
        'fileName':optimizableLoops[loopSection]['fileName'],
        'identifier':loopSection,
        'startLine': optimizableLoops[loopSection]['startLine'],
        'endLine':optimizableLoops[loopSection]['endLine'],
        'executionTime':optimizableLoops[loopSection]['sectionTime'],
        'optimiazability':False,
        'optimizedTime':0,
        'optimizeMethod':None
        }
        if(float(optimizableLoops[loopSection]['overheadPrecentage'])> 0.0):
            selectedSection['optimiazability'] = True
            summarySection['optimiazability'] = True
        summaryLoops.append(summarySection)
        selectedLoops.append(selectedSection)
    dbManager.write('summaryLoops',summaryLoops)
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

    logger.loggerInfo("Profile Summarization Initiated")
    summarizedReport = getSummary(directory,dbManager.read('runTimeArguments'))
    if summarizedReport['returncode'] == 1:
        logger.loggerSuccess("Profile Summarization completed successfully")
        loopSections = selectOptimizableLoopSections(summarizedReport['content'])
        dbManager.overWrite('loopSections', loopSections)
        if (len(loopSections)>0):
            isGpu = True
            isVector = True
            if bool(responseObj['content']['gpuinfo']): #check Gpu Info
                logger.loggerInfo("Feature Extraction for GPU Initiated")
                dbManager.write('gpuopt',True)
                gpuThread = threading.Thread(target=gpuAnalzyer,args=(extractor,directory,loopSections,))
                gpuThread.start()
            else:
                isGpu = False
                dbManager.write('gpuopt',False)
                logger.loggerInfo("No GPU found. GPU offloading will be skipped")
            if (responseObj['content']['cpuinfo']['vectorization']): #check Vectorization optimizations
                logger.loggerInfo("Available Vector Instructions")
                #display what Instructions available
                logger.loggerInfo("Feature Extraction for Vectorization Initiated")
                dbManager.write('vecopt',True)
                vectorThread = threading.Thread(target=vecAnalzyer,args=(extractor,directory,loopSections,))
                vectorThread.start()
            else:
                isVector = False
                dbManager.write('vecopt',False)
                logger.loggerInfo("No Vector Instructions were found. Skip Vector optimizations")

            if (isGpu):
                if (isVector):
                    gpuThread.join()
                    vectorThread.join()
                    loopSectionsTemp = dbManager.read('loopSectionsTemp')
                    dbManager.overWrite('loopSections', loopSectionsTemp)
                    logger.loggerInfo("GPU and Vector Optimizations Considered")
                    response['content'] = {'cosidered':'both', 'status':True}
                    response["returncode"] = 0

                else:
                    gpuThread.join()
                    loopSectionsTemp = dbManager.read('loopSectionsTemp')
                    dbManager.overWrite('loopSections', loopSectionsTemp)
                    logger.loggerInfo("Only GPU Optimizations Considered.")
                    response['content'] = {'cosidered':'GPU', 'status':True}
                    response["returncode"] = 0
            else:
                if (isVector):
                    vectorThread.join()
                    loopSectionsTemp = dbManager.read('loopSectionsTemp')
                    dbManager.overWrite('loopSections', loopSectionsTemp)
                    logger.loggerInfo("Only Vector Optimizations Considered.")
                    response['content'] = {'cosidered':'Vector', 'status':True}
                    response["returncode"] = 0

                else:
                    logger.loggerInfo("No additional hardware support is found for optimizations. only CPU optimizations will be considered.")
                    response['content'] = {'cosidered':'None', 'status':True}
                    response["returncode"] = 0

        else:
            logger.loggerInfo("No significant loops available for optimization. Optimization process terminated.")
            response['content'] = {'cosidered':'NoOpt', 'status':True}
            response["returncode"] = 0
    else:
        logger.loggerError("Profile Summarization Failed. Optimization process terminated.")
        print "Profile Summarization Failed. Optimization process terminated."
        response['content'] = {'cosidered':'', 'status':False}
        response["returncode"] = 1

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
        response['returnCode'] = 0
    return response
