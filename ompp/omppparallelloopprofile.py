import os
import sys
import re

def getParallelLoopSummary(dataSumArray,dataArray):
    response ={
        'returncode':0,
        'content':{},
        'error':""
    }

    try:
        keyList = []
        if('PARALLEL LOOP' in  dataSumArray ):
            keyList = dataSumArray['PARALLEL LOOP']['regions'].keys()
        if ('LOOP' in dataSumArray):
            keyList = keyList + dataSumArray['LOOP']['regions'].keys()
        for region in keyList:

            initLine = dataArray.index('##BEG '+region+' flat profile')
            endLine = dataArray.index('##END '+region+' flat profile')
            threadData = {}

            for i in range(initLine+3, endLine, 1):
                dataArrayRow = dataArray[i].split(',')
                for emptyCheck in range(len(dataArrayRow),7):
                    dataArrayRow.append("None")
                threadData[dataArrayRow[0]] = {"execT":dataArrayRow[1],"execC":dataArrayRow[2],"bodyT":dataArrayRow[3],"exitBarT":dataArrayRow[4],"startupT":dataArrayRow[5],"shutdwnT":dataArrayRow[6]}

            intiLineOverall = dataArray.index('##BEG overheads for parallel region')
            endLineOverall = dataArray.index('##END overheads for parallel region')
            overallData = {}
            for j in range(intiLineOverall+2, endLineOverall, 1):
                overallDataSet = dataArray[j].split(',')
                if(overallDataSet[0] ==region ):
                    overallData = {"Total":overallDataSet[1],"Ovhds":overallDataSet[2],"OvhdsP":overallDataSet[3],"Synch":overallDataSet[4],"SynchP":overallDataSet[5],"Imbal":overallDataSet[6],"ImbalP":overallDataSet[7],"Limpar":overallDataSet[8],"LimparP":overallDataSet[9],"Mgmt":overallDataSet[10],"MgmtP":overallDataSet[11]}
                    break
            intiLineOverallProg = dataArray.index('##BEG overheads for whole program')
            endLineOverallProg = dataArray.index('##END overheads for whole program')
            overallDataProg = {}
            for k in range(intiLineOverallProg+2, endLineOverallProg-1, 1):
                overallDataProgSet = dataArray[k].split(',')
                if(overallDataProgSet[0] ==region ):
                    overallDataProg = {"Total":overallDataProgSet[1],"Ovhds":overallDataProgSet[2],"OvhdsP":overallDataProgSet[3],"Synch":overallDataProgSet[4],"SynchP":overallDataProgSet[5],"Imbal":overallDataProgSet[6],"ImbalP":overallDataSet[7],"Limpar":overallDataProgSet[8],"LimparP":overallDataProgSet[9],"Mgmt":overallDataProgSet[10],"MgmtP":overallDataProgSet[11]}
                    break
            response['content'][region] = {'threadData': threadData,'overallData' : overallData,'overallProgramData':overallDataProg}
            response['error'] = ""
            response['returncode'] = 1

    except Exception as e:
        print e
        print "Unexpected Error Occured."
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
    return response
