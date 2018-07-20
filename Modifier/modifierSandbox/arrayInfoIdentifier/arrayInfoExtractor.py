import logger,os,shutil
from arrayInfoFetcher import arrayInfoFetch

def arrayInfoExtract(filePath,startLine,endLine):
    result = {
        'code':0,
        'content':[],
        'error':'',
        }
    logger.loggerInfo("Array Information Fetch Command Initiated")
    if (os.path.isfile(filePath)):
        subFilePath = filePath.split("Sandbox")[1]
        subFileMainPath = filePath.split("Sandbox")[0]+"Sandbox/"+subFilePath.split('/')[1]
        if(os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/"+subFilePath.split('/')[1])):
            shutil.rmtree(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/"+subFilePath.split('/')[1])
        shutil.copytree(subFileMainPath, os.path.dirname(os.path.realpath(__file__))+"/Sandbox/"+subFilePath.split('/')[1])
        resultLocal = arrayInfoFetch(subFilePath,startLine,endLine)
        if (resultLocal["code"]):
            result['code']=0
            result['content']=resultLocal['data']
            result['error']=''
        else:
            result['code']=1
            result['content']=[]
            result['error']=resultLocal["error"]
    else:
        result['code']=1
        result['content']=[]
        result['error']="unable to find file : " + filePath
    return result
