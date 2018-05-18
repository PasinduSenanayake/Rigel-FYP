from Extractor import Extractor
from ComponentAPIs.setScheduler import setSchedule


def setPragmaSchedule(fileName, mechanism, lineNumber = None):
    response = {
    "returncode":0,
    "error":"",
    "content":{}
    }
    if(fileName == None):
        response['error']='FileName is missing'
        return response

    if(mechanism == None):
        response['error']='Schduling mechanism is missing'
        return response

    extractor = Extractor()
    sourceObj = extractor.addSource(fileName)
    if (lineNumber== None):
        setSchedule(sourceObj,mechanism)
    else:
        setSchedule(sourceObj,mechanism,lineNumber)
    sourceObj.writeToFile(fileName.rsplit('.', 1)[0]+"Static.c")
    response['returncode']=1
    return response;
