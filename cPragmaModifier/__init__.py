from Extractor import Extractor
from ComponentAPIs.setScheduler import setSchedule


def setPragmaSchedule(fileName,alteredFileName, mechanism, lineNumber = None):
    response = {
    "returncode":0,
    "error":"",
    "content":{}
    }
    if(fileName == None):
        response['error']='FileName is missing'
        return response
    if(alteredFileName == None):
        response['error']='Altered FileName is missing'
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
    sourceObj.writeToFile(alteredFileName)
    response['returncode']=1
    return response;
