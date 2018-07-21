import pandas as pd
import math,os,json
import logger

branchDataList = []
fileLocation = os.path.dirname(os.path.realpath(__file__))+"/Sandbox"

def preBranchDataFetch(fileName):
    global fileLocation
    fileLocation = fileLocation+fileName.rsplit('/', 1)[0]+"/"
    try:
        df = pd.read_csv(fileLocation+"branch_profiling.csv")
        dataSet = {}
        uniqueData =  df['pc'].unique()
        for unique in uniqueData:
            dataSet[unique] =  ",".join(df.loc[df['pc'] == unique,'branch'])
        newCsv = pd.DataFrame(list(dataSet.iteritems()),columns=['pc', 'branchValues'])
        newCsv.to_csv(fileLocation+"categorizedBranchProfileData.csv")
        return True
    except Exception as e:
        logger.loggerError.debug("branch_profiling.csv info fetching failed with Error : "+str(e))
        return False

def fetchBranchInfo():
    try:
        odf = pd.read_csv(fileLocation+"categorizedBranchProfileData.csv")
        resultDataSet = odf.to_dict(orient='records')
        for resultData in resultDataSet:
            branchData = {}
            for interval in [16,32,64,128,256,512,1024]:
                subRowSet =  resultData['branchValues'].split(',')
                branchData[interval]={}
                tempLength = len(subRowSet)
                branchData[interval]["size"] = len(subRowSet)
                totalValue = 0
                value = 0
                for i in range (0,int(math.ceil(len(subRowSet)/float(interval)))):
                    if(tempLength>=interval):
                        newLoop = True
                        isSameType = False
                        branchType ="N"
                        for j in range (i*interval, (i+1)*interval):
                            if(newLoop):
                                branchType = subRowSet[j]
                                newLoop = False
                            else:
                                if (subRowSet[j] == branchType):
                                    isSameType = True
                                else:
                                    isSameType = False
                                    break
                        if not (isSameType):
                            value = value +1
                        totalValue = totalValue +1
                    tempLength = tempLength -interval
                branchData[interval]["jump_count"] = value
                branchData[interval]["total_count"] = totalValue
                if(totalValue>0):
                    branchData[interval]["ratio"] = float(value)/float(totalValue)
                else:
                    branchData[interval]["ratio"]  = 0.0
            branchDataList.append(branchData)
        with open(fileLocation+'branching.json', 'w') as outfile:
            json.dump(branchDataList, outfile)
        return True
    except Exception as e:
        logger.loggerError.debug("Branching info extraction failed with Error : "+str(e))
        return False
