import pandas as pd
import math

subProfileShMemBW = {
    "broadCast":0,
    "stride 2":0,
    "stride 4":0,
    "stride 8":0,
    "stride 16":0,
    "stride 32":0,
    "stride odd":0
    }

def preMemoryMapping():
    df = pd.read_csv("profiling.csv")
    dataSet = {}
    uniqueData =  df['pc'].unique()
    for unique in uniqueData:
        dataSet[unique] =  ",".join(df.loc[df['pc'] == unique,'address_size'])
    newCsv = pd.DataFrame(list(dataSet.iteritems()),columns=['pc', 'address_sizes'])
    newCsv.to_csv("categorizedProfileData.csv")


def sharedMemoryMapping():
    odf = pd.read_csv("categorizedProfileData.csv")
    resultDataSet = odf.to_dict(orient='records')
    for resultData in resultDataSet:
        subRowSet =  resultData['address_sizes'].split(',')
        tempLength = len(subRowSet)
        for i in range (0,int(math.ceil(len(subRowSet)/32.0))):
            if(tempLength>=32):
                stride = 0
                newLoop = True
                changeStride = False
                for j in range (i*32+1, (i+1)*32):
                    if(newLoop):
                        stride = abs(int(subRowSet[j].split('+')[0].split('x')[1],16)-(int(subRowSet[j-1].split('+')[0].split('x')[1],16)+int(subRowSet[j-1].split('+')[1].split('x')[1],16)))
                        newLoop = False
                    else:
                        if (abs(int(subRowSet[j].split('+')[0].split('x')[1],16)-(int(subRowSet[j-1].split('+')[0].split('x')[1],16)+int(subRowSet[j-1].split('+')[1].split('x')[1],16))) == stride):
                            changeStride = False
                        else:
                            changeStride = True
                            break
                if not changeStride:
                    if(stride/4 == 0):
                        subProfileShMemBW["broadCast"] = subProfileShMemBW["broadCast"]+1
                    elif(stride/4 == 2):
                        subProfileShMemBW["stride 2"] = subProfileShMemBW["stride 2"]+1
                    elif(stride/4 == 4):
                        subProfileShMemBW["stride 4"] = subProfileShMemBW["stride 4"]+1
                    elif(stride/4 == 8):
                        subProfileShMemBW["stride 8"] = subProfileShMemBW["stride 8"]+1
                    elif(stride/4 == 16):
                        subProfileShMemBW["stride 16"] = subProfileShMemBW["stride 16"]+1
                    elif(stride/4 == 32):
                        subProfileShMemBW["stride 32"] = subProfileShMemBW["stride 32"]+1
                    elif((stride/4) % 2 == 1):
                        subProfileShMemBW["stride odd"] = subProfileShMemBW["stride odd"]+1
                tempLength = tempLength -32
    return subProfileShMemBW

#
# odf = pd.read_csv("categorizedProfileData.csv")
# resultDataSet = odf.to_dict(orient='records')
# for resultData in resultDataSet:
#     subRowSet =  resultData['addresses'].split(',')
#     tempLength = len(subRowSet)
#     for i in range (0,int(math.ceil(len(subRowSet)/32.0))):
#         if(tempLength>=32):
#             partialDataSet = []
#             for j in range (i*32, (i+1)*32):
#                 partialDataSet.append(subRowSet[j])
#
#             tempLength = tempLength -32
