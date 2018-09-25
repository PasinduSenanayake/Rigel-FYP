import os
import dbManager
from InitialExecutor.initExecutor import initExecution
from FinalExecutor.finalExecutor import finalExecution

def initExecutor(dirPath,runTimeArguments):
    response = {
        "error":"",
        "content":{},
        "returncode":0
        }
    returnResponse = initExecution(dirPath,runTimeArguments)
    if (returnResponse['returncode']==0):
        response['error'] ='Program terminated due to a runtime error'
        if returnResponse['error'] =="":
            response['content'] =returnResponse['error']
        else:
            response['content'] =returnResponse['content']
    response['returncode'] = returnResponse['returncode']
    return response

def finalExecutor(dirPath,runTimeArguments):
    response = {
        "error":"",
        "content":{},
        "returncode":0
        }
    returnResponse = finalExecution(dirPath,runTimeArguments)
    if (returnResponse['returncode']==0):
        response['error'] ='Program terminated due to a runtime error'
        if returnResponse['error'] =="":
            response['content'] =returnResponse['error']
        else:
            response['content'] =returnResponse['content']
    response['returncode'] = returnResponse['returncode']
    return response


def visualizerExecutor():
    return 0;
