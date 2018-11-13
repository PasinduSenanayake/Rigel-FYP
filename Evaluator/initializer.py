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
    noTime = 2.33
    loopNames = []
    nonOptLoopTimes = []
    optLoopTimes = []
    summaryLoops = dbManager.read('summaryLoops')
    totalExetime =  dbManager.read('iniExeTime')
    for summaryLoop in summaryLoops:
        if summaryLoop['optimiazability'] :
            loopNames.append(summaryLoop['startLine']+":"+summaryLoop['endLine'])
            nonOptLoopTimes.append(float(summaryLoop['executionTime']))
            if summaryLoop['optimizeMethod'] == 'GPU':
                gpuTime = gpuTime + float(summaryLoop['executionTime'])
                optLoopTimes.append(float(summaryLoop['optimizedTime']))
            elif summaryLoop['optimizeMethod'] == 'vector':
                vecTime = vecTime + float(summaryLoop['executionTime'])
                optLoopTimes.append(float(dbManager.read('vecOptTime')))
            elif summaryLoop['optimizeMethod'] == None :
                cpuTime = cpuTime + float(summaryLoop['executionTime'])
                optLoopTimes.append(float(summaryLoop['optimizedTime']))
        else:
            noTime = noTime + summaryLoop['executionTime']


    reportObj = {}
    reportObj['totalExeTime'] = totalExetime
    reportObj['gpuOptTime'] = gpuTime
    reportObj['cpuOptTime'] = cpuTime
    reportObj['vecOptTime'] = vecTime
    reportObj['notOptTime'] = noTime
    reportObj['toverhead'] = float(dbManager.read('GPU_OptTime'))+float(dbManager.read('gpuFeatureTime')) + float(dbManager.read('schedulerExeTime'))+float(dbManager.read('Vec_OptTime'))
    reportObj['gpuExeTime'] = float(dbManager.read('GPU_OptTime'))+float(dbManager.read('gpuFeatureTime'))
    reportObj['cpuExeTime'] = float(dbManager.read('schedulerExeTime'))
    reportObj['vecExeTime'] = float(dbManager.read('Vec_OptTime')) + float(dbManager.read('vecFeatureTime'))
    reportObj['loopLines'] = loopNames
    reportObj['notOptLoopTimes'] = nonOptLoopTimes
    reportObj['optLoopTimes'] = optLoopTimes
    reportGenerator(reportObj)
    return 0;
