from omppNew.omppbasicprofile import getBasicProfile

def getSummary(filePath,runTimeArguments):
    returnResponse = {
    "returncode" :1,
    "content" : [],
    "error" : ""
    }
    response = getBasicProfile(filePath,runTimeArguments)
    if response['returncode'] == 1:
        summarizedReport={}
        dataArray = response['content']
        initLine = dataArray.index('##BEG overheads for whole program')
        endLine = dataArray.index('##END overheads for whole program')
        for i in range(initLine+2, endLine, 1):
            if not(dataArray[i].split(',')[0] == 'SUM'):
                summarizedReport[dataArray[i].split(',')[0]]={'TotalTime':dataArray[i].split(',')[1],'sectionTime':dataArray[i].split(',')[2],'overheadPrecentage':dataArray[i].split(',')[3],'startLine':'','endLine':''}
        initLine = dataArray.index('##BEG region overview')
        endLine = dataArray.index('##END region overview')
        for i in range(initLine+2, endLine, 1):
                summarizedReport[dataArray[i].split(',')[0]]['fileName']=dataArray[i].split(',')[2]
                summarizedReport[dataArray[i].split(',')[0]]['startLine']=dataArray[i].split(',')[3]
                summarizedReport[dataArray[i].split(',')[0]]['endLine']=dataArray[i].split(',')[4]
        returnResponse['content'] =summarizedReport
    else:
        returnResponse['content'] = ""
    returnResponse['returncode'] = response['returncode']
    returnResponse['error'] = response['error']
    return returnResponse
