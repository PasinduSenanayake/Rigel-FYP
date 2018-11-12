import os
import dbManager
from InitialExecutor.initExecutor import initExecution
from FinalExecutor.finalExecutor import finalExecution
from visualizer import reportGenerator

def initExecutor(dirPath,runTimeArguments):
    response = {
        "error":"",
        "content":{},
        "returncode":0
        }
    returnResponse = initExecution(dirPath,runTimeArguments)
    if (returnResponse['returncode']==0):
        response['error'] ='Program terminated due to a runtime error'
        if returnResponse['error'] == "":
            response['content'] = returnResponse['error']
        else:
            response['content'] = returnResponse['content']
    response['returncode'] = returnResponse['returncode']
    return response

def finalExecutor(dirPath,runTimeArguments, additionalFlags = ""):
    response = {
        "error": "",
        "content": {},
        "returncode": 0
        }
    returnResponse = finalExecution(dirPath,runTimeArguments, additionalFlags)
    if (returnResponse['returncode']==0):
        response['error'] ='Program terminated due to a runtime error'
        if returnResponse['error'] != "":
            response['content'] = returnResponse['error']
        else:
            response['content'] = returnResponse['content']
    response['returncode'] = returnResponse['returncode']
    return response


def visualizerExecutor():
    vecTime = 0
    gpuTime = 0
    cpuTime = 0
    noTime = 0
    loopNames = []
    nonOptLoopTimes = []
    optLoopTimes = []
    summaryLoops = dbManager.read('summaryLoops')
    totalExetime =  dbManager.read('iniExeTime')

    for summaryLoop in summaryLoops:
        if summaryLoop['optimiazability'] :
            if summaryLoop['optimizeMethod'] == 'GPU':
                gpuTime = gpuTime + float(summaryLoop['executionTime'])
            elif summaryLoop['optimizeMethod'] == 'Vec':
                vecTime = vecTime + float(summaryLoop['executionTime'])
            elif summaryLoop['optimizeMethod'] == None :
                cpuTime = cpuTime + float(summaryLoop['executionTime'])
            loopNames.append(summaryLoop['startLine']+":"+summaryLoop['endLine'])
            nonOptLoopTimes.append(float(summaryLoop['executionTime']))
            optLoopTimes.append(float(summaryLoop['optimizedTime']))
        else:
            noTime = noTime + summaryLoop['executionTime']

    reportObj = {}
    reportObj['totalExeTime'] = totalExetime
    reportObj['gpuOptTime'] = gpuTime
    reportObj['cpuOptTime'] = cpuTime
    reportObj['vecOptTime'] = vecTime
    reportObj['notOptTime'] = noTime
    reportObj['gpuExeTime'] = float(dbManager.read('GPU_OptTime'))
    reportObj['cpuExeTime'] = float(dbManager.read('schedulerExeTime'))
    reportObj['vecExeTime'] = 0
    reportObj['loopLines'] = loopNames
    reportObj['notOptLoopTimes'] = nonOptLoopTimes
    reportObj['optLoopTimes'] = optLoopTimes
    reportGenerator(reportObj)
    return 0;
