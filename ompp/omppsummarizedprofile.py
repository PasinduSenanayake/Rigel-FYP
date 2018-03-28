import os
import sys
import re

def getSummarizedProfile(dataArray):
    summarizedReport={}
    response ={
        'returncode':0,
        'content':{},
        'error':""
    }
    try:
        initLine = dataArray.index('##BEG region overview')
        endLine = dataArray.index('##END region overview')
        pattern = re.compile("^[a-zA-Z][0-9]{5}$")
        tempName = ""
        for i in range(initLine+1, endLine, 1):
            if not(pattern.match(dataArray[i].split(',')[0])):
                summarizedReport[dataArray[i].split(',')[0]]={'regions':{},'regionsCount':dataArray[i].split(',')[1]}
                tempName = dataArray[i].split(',')[0]
            else:
                tempRow ={'startLine':dataArray[i].split(',')[3],'endLine':dataArray[i].split(',')[4]}
                summarizedReport[tempName]['regions'][dataArray[i].split(',')[0]]= tempRow
        response['content'] = summarizedReport
        response['error']=""
        response['returncode'] = 1
    except Exception as e:
        print e
        print "Unexpected Error Occured."
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
    return response
