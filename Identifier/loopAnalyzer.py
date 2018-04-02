import re
import ompp

response = {
    "returncode":0,
    "error":"",
    "content":{}
}

def loopAnalysis(filePath, compTimeArguments, runTimeArguments):
    try:
        if not (filePath == None ):
            parallelDataArray =  ompp.getParallelLoopData(filePath,compTimeArguments = compTimeArguments,runTimeArguments = runTimeArguments)
            for region in parallelDataArray['content'].keys():
                if(float(parallelDataArray['content'][region]['threadData']['SUM']['execT'])>3):
                    if('ImbalP' in parallelDataArray['content'][region]['overallData']):
                        if(float(parallelDataArray['content'][region]['overallData']['ImbalP'])>6.0 and float(parallelDataArray['content'][region]['overallProgramData']['ImbalP'])>1):
                            threadTimeDataKey=[]
                            threadTimeData=[]
                            for threadData in parallelDataArray['content'][region]['threadData'].keys():
                                if not (threadData == "SUM"):
                                    threadTimeDataKey.append(int(threadData))
                            for threadNumber in sorted(threadTimeDataKey, key=int):
                                threadTimeData.append(float(parallelDataArray['content'][region]['threadData'][str(threadNumber)]['bodyT']))
                            if(threadTimeData == sorted(threadTimeData, key=int)):
                                print "Change into Guided"
                                response['error'] = ""
                                response['content'] = "Change into Guided"
                                response['returncode'] = 1
                            elif (threadTimeData == sorted(threadTimeData, key=int, reverse=True)):
                                print "Change into Guided - Reverse the Loop"
                                response['error'] = ""
                                response['content'] = "Change into Guided - Reverse the Loop"
                                response['returncode'] = 1
                            else:
                                print "change into dynamic"
                                response['error'] = ""
                                response['content'] = "change into dynamic"
                                response['returncode'] = 1
                        else:
                            print "Keep Static - increament of number of threads by 1 is favourable"
                            response['error'] = ""
                            response['content'] = "Keep Static - increament of number of threads by 1 is favourable"
                            response['returncode'] = 1
                    else:
                        threadTimeDataKey=[]
                        threadTimeData=[]
                        if( (float(parallelDataArray['content'][region]['threadData']['SUM']['exitBarT']) / float(parallelDataArray['content'][region]['threadData']['SUM']['bodyT']) * 100)>10 ):
                            for threadData in parallelDataArray['content'][region]['threadData'].keys():
                                if not (threadData == "SUM"):
                                    threadTimeDataKey.append(int(threadData))
                            for threadNumber in sorted(threadTimeDataKey, key=int):
                                threadTimeData.append(float(parallelDataArray['content'][region]['threadData'][str(threadNumber)]['bodyT']))
                            if(threadTimeData == sorted(threadTimeData, key=int)):
                                print "Change into Guided"
                                response['error'] = ""
                                response['content'] = "Change into Guided"
                                response['returncode'] = 1
                            elif (threadTimeData == sorted(threadTimeData, key=int, reverse=True)):
                                print "Change into Guided - Reverse the Loop"
                                response['error'] = ""
                                response['content'] = "Change into Guided - Reverse the Loop"
                                response['returncode'] = 1
                            else:
                                print "change into dynamic"
                                response['error'] = ""
                                response['content'] = "change into dynamic"
                                response['returncode'] = 1
                        else:
                            print "Keep Static"
                            response['error'] = ""
                            response['content'] = "Keep Static"
                            response['returncode'] = 1
                else:
                    print "Loop is not significant for optimizations"
                    response['error'] = ""
                    response['content'] = "Loop is not significant for optimizations"
                    response['returncode'] = 1
            else :
                response['error'] = "File path is required"
                response['content'] = {}
                response['returncode'] = 0
    except Exception as e:
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
    return response
