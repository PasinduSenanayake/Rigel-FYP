from Identifier.nestedLoopChecker import nestedloopAnalysis
from loopAnalyzer import loopAnalysis
from systemIdentifier.systemIdentifier import __systemInformationIdentifier
import dbManager,logger

response = {
    "returncode":0,
    "error":"",
    "content":{}
    }

def identify(extractor,directory):
    global response
    try:
        logger.loggerInfo("System Information Fetcher Initiated")
        responseObj = __systemInformationIdentifier()
        if(responseObj['returncode']==1):
            dbManager.write('systemData',responseObj['content'])
            logger.loggerSuccess("System Information Fetcher completed successfully")
        else:
            logger.loggerError("System Information Fetcher Failed")

    except Exception as e:
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
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
