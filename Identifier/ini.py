from loopAnalyzer import loopAnalysis

response = {
    "returncode":0,
    "error":"",
    "content":{}
    }

def trigger(filePath,compTimeArguments,runTimeArguments):
    try:
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
