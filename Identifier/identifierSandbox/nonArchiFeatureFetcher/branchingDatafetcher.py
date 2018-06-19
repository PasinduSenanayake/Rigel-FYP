import pandas as pd
import math


def branchCollector():
    df = pd.read_csv("branch_profiling.csv")
    dataSet = {}
    uniqueData =  df['pc'].unique()
    for unique in uniqueData:
        dataSet[unique] =  ",".join(df.loc[df['pc'] == unique,'branch'])
    newCsv = pd.DataFrame(list(dataSet.iteritems()),columns=['pc', 'branchValues'])
    newCsv.to_csv("categorizedBranchProfileData.csv")

    value = 0
    TotalValue = 0
    odf = pd.read_csv("categorizedBranchProfileData.csv")
    resultDataSet = odf.to_dict(orient='records')
    for resultData in resultDataSet:
        subRowSet =  resultData['branchValues'].split(',')
        tempLength = len(subRowSet)
        for i in range (0,int(math.ceil(len(subRowSet)/32.0))):
            if(tempLength>=32):
                newLoop = True
                isSameType = False
                branchType ="N"
                for j in range (i*32, (i+1)*32):
                    if(newLoop):
                        branchType = subRowSet[j]
                        newLoop = False
                    else:
                        if (subRowSet[j] == branchType):
                            isSameType = True
                        else:
                            isSameType = False
                            break
                if(isSameType):
                    value = value +1
                TotalValue = TotalValue +1
                tempLength = tempLength -32
    return {"alinged":value, "total":TotalValue}
