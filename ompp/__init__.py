from .omppbasicprofile import getBasicProfile
from .omppsummarizedprofile import getSummarizedProfile
from .omppparallelloopprofile import getParallelLoopSummary

def getParallelLoopData(filePath, compTimeArguments="",runTimeArguments=""):
    response = {
        "error":"",
        "content":{},
        "returncode":0
        }
    try:
        dataArray  = getBasicProfile(filePath,compTimeArguments=compTimeArguments,runTimeArguments=runTimeArguments)
        if not (dataArray['returncode'] == 0):
            dataSumArray = getSummarizedProfile(dataArray['content'])
            if not (dataSumArray['returncode'] == 0):
                parallelDataArray = getParallelLoopSummary(dataSumArray['content'],dataArray['content'])
                if not (parallelDataArray['returncode'] == 0):
                    response['content']= parallelDataArray['content']
                    response['error'] = ""
                    response['returncode'] = 1
                else:
                    response['content']={}
                    response['error'] = parallelDataArray['error']
                    response['returncode'] = 0
            else:
                response['content']={}
                response['error'] = dataSumArray['error']
                response['returncode'] = 0
        else:
            response['content']={}
            response['error'] = dataArray['error']
            response['returncode'] = 0
    except Exception as e:
        print e
        print "Unexpected Error Occured."
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
    return response
