from loopAnalyzer import loopAnalysis
from systemIdentifier import __systemInformationIdentifier
response = {
    "returncode":0,
    "error":"",
    "content":{}
    }

def trigger(filePath,compTimeArguments,runTimeArguments):
    try:
        responseObj = __systemInformationIdentifier()
        if responseObj['returncode'] == 1:
            responseObj = loopAnalysis(filePath,compTimeArguments,runTimeArguments)
            if (responseObj['returncode'] == 1):
                response['error'] = ""
                response['content'] = responseObj['content']
                response['returncode'] = 1
    except Exception as e:
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
    return response
