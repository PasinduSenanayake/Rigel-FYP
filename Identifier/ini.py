from Identifier.nestedLoopChecker import nestedloopAnalysis
from loopAnalyzer import loopAnalysis
from systemIdentifier import __systemInformationIdentifier
import cPragmaModifier
response = {
    "returncode":0,
    "error":"",
    "content":{}
    }

def trigger(filePath,compTimeArguments,runTimeArguments):

    try:
        responseObj = __systemInformationIdentifier()
        if responseObj['returncode'] == 1:
            responseObj = cPragmaModifier.setPragmaSchedule(filePath,filePath.rsplit('.',1)[0]+'Static.c','static')
            if responseObj['returncode'] == 1:
                responseObj = loopAnalysis(filePath.rsplit('.',1)[0]+'Static.c',compTimeArguments,runTimeArguments)
                if (responseObj['returncode'] == 1):
                    response['error'] = ""
                    response['content'] = responseObj['content']
                    response['returncode'] = 1
                else
                    response = responseObj
            else
                response = responseObj
        else
            response = responseObj
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
