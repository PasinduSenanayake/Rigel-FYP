import pandas as pd
import math,os,json,logger

branchDataList = []
fileLocation = os.path.dirname(os.path.realpath(__file__))+"/Sandbox"

def preCollapseBranchDataFetch(fileName):
    global fileLocation
    fileLocation = fileLocation+fileName.rsplit('/', 1)[0]+"/"
        # df = pd.read_csv(fileLocation+"branch_profiling.csv")
        # dataSet = {}
        # uniqueData =  df['pc'].unique()
        # for unique in uniqueData:
        #     dataSet[unique] =  ",".join(map(str,df.loc[df['pc'] == unique,'branch']))
        # newCsv = pd.DataFrame(list(dataSet.iteritems()),columns=['pc', 'branchValues'])
        # newCsv.to_csv(fileLocation+"categorizedCollapseBranchProfileData.csv")
        # return True
    try:
        totalPastRows = 0
        decide = 0
        os.rename(fileLocation+"/branch_profiling.csv", fileLocation+"/branch_profiling_new0.csv")
        while (True):
            totalRows = 0
            inloop = False
            for chunk in  pd.read_csv(fileLocation+"/branch_profiling_new"+str(decide)+".csv", chunksize=10000000):
                if not(inloop):
                    decide = decide +1
                    inloop = True
                df = chunk
                dataSet = {}
                uniqueData =  df['pc'].unique()
                for unique in uniqueData:
                    dataSet[unique] =  ",".join(map(str,df.loc[df['pc'] == unique,'branch']))
                newCsv = pd.DataFrame(list(dataSet.iteritems()),columns=['pc', 'branch'])
                totalRows = totalRows+ len(newCsv.index)
                if not os.path.isfile(fileLocation+"/branch_profiling_new"+str(decide)+".csv"):
                    newCsv.to_csv(fileLocation+"/branch_profiling_new"+str(decide)+".csv")
                else:
                    newCsv.to_csv(fileLocation+"/branch_profiling_new"+str(decide)+".csv", mode='a', header=False)
            if (totalRows == totalPastRows):
                os.remove(fileLocation+"/branch_profiling_new"+str(decide-1)+".csv")
                os.rename(fileLocation+"/branch_profiling_new"+str(decide)+".csv", fileLocation+"/categorizedCollapseBranchProfileData.csv")
                break
            else:
                os.remove(fileLocation+"/branch_profiling_new"+str(decide-1)+".csv")
                totalPastRows = totalRows
        return True
    except Exception as e:
        logger.loggerError("branch_profiling.csv info fetching failed with Error : "+str(e))
        return False

def fetchCollapseBranchInfo(fileName):
    global fileLocation
    branchDataList = []
    fileLocation = fileLocation+fileName.rsplit('/', 1)[0]+"/"
    try:
        odf = pd.read_csv(fileLocation+"branch_profiling.csv")
        resultDataSet = odf.to_dict(orient='records')
        for resultData in resultDataSet:
            branchData = {}
            for interval in ['16','32','64','128','256','512','1024']:
                branchData[interval]={}
                branchData[interval]["size"] = int(resultData['size'])
                branchData[interval]["jump_count"] = int(resultData[interval].split(':')[0])
                branchData[interval]["total_count"] = int(resultData[interval].split(':')[1])
                if(branchData[interval]["total_count"]>0):
                    branchData[interval]["ratio"] = float(branchData[interval]["jump_count"])/float(branchData[interval]["total_count"])
                else:
                    branchData[interval]["ratio"]  = 0.0
            branchDataList.append(branchData)
        with open(fileLocation+'branching_collapse.json', 'w') as outfile:
            json.dump(branchDataList, outfile)
        return True
    except Exception as e:
        logger.loggerError("Branching info extraction failed with Error : "+str(e))
        return False



# def fetchCollapseBranchInfo():
#     try:
#         odf = pd.read_csv(fileLocation+"categorizedCollapseBranchProfileData.csv")
#         resultDataSet = odf.to_dict(orient='records')
#         for resultData in resultDataSet:
#             branchData = {}
#             for interval in [16,32,64,128,256,512,1024]:
#                 subRowSet =  resultData['branch'].split(',')
#                 branchData[interval]={}
#                 tempLength = len(subRowSet)
#                 branchData[interval]["size"] = len(subRowSet)
#                 totalValue = 0
#                 value = 0
#                 for i in range (0,int(math.ceil(len(subRowSet)/float(interval)))):
#                     if(tempLength>=interval):
#                         newLoop = True
#                         isSameType = False
#                         branchType ="0"
#                         for j in range (i*interval, (i+1)*interval):
#                             if(newLoop):
#                                 branchType = subRowSet[j]
#                                 newLoop = False
#                             else:
#                                 if (subRowSet[j] == branchType):
#                                     isSameType = True
#                                 else:
#                                     isSameType = False
#                                     break
#                         if not (isSameType):
#                             value = value +1
#                         totalValue = totalValue +1
#                     tempLength = tempLength -interval
#                 branchData[interval]["jump_count"] = value
#                 branchData[interval]["total_count"] = totalValue
#                 if(totalValue>0):
#                     branchData[interval]["ratio"] = float(value)/float(totalValue)
#                 else:
#                     branchData[interval]["ratio"]  = 0.0
#             branchDataList.append(branchData)
#         with open(fileLocation+'branching_collapse.json', 'w') as outfile:
#             json.dump(branchDataList, outfile)
#         return True
#     except Exception as e:
#         logger.loggerError.debug("Branching info extraction failed with Error : "+str(e))
#         return False
