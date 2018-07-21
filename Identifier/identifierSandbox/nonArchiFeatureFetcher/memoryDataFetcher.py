import pandas as pd
import math,os,logger

fileLocation = os.path.dirname(os.path.realpath(__file__))+"/Sandbox"

subProfileShMemBW = {
    "broadCast":0,
    "stride 2":0,
    "stride 4":0,
    "stride 8":0,
    "stride 16":0,
    "stride 32":0,
    "stride odd":0
    }

subProfileGMemBW = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

global totalWindowNumber
totalWindowNumber = 0
def preMemoryMapping(fileName):
    global fileLocation
    fileLocation = fileLocation+fileName.rsplit('/', 1)[0]+"/"
    try:
        df = pd.read_csv(fileLocation+"memory_profiling_fread.csv")
        dataSet = {}
        uniqueData =  df['pc'].unique()
        for unique in uniqueData:
            dataSet[unique] =  ",".join(df.loc[df['pc'] == unique,'address'])
        newCsv = pd.DataFrame(list(dataSet.iteritems()),columns=['pc', 'addresses'])
        newCsv.to_csv(fileLocation+"categorized_memory_fr_profiling.csv")

        df = pd.read_csv(fileLocation+"memory_profiling_sread.csv")
        dataSet = {}
        uniqueData =  df['pc'].unique()
        for unique in uniqueData:
            dataSet[unique] =  ",".join(df.loc[df['pc'] == unique,'address'])
        newCsv = pd.DataFrame(list(dataSet.iteritems()),columns=['pc', 'addresses'])
        newCsv.to_csv(fileLocation+"categorized_memory_sr_profiling.csv")

        df = pd.read_csv(fileLocation+"memory_profiling_write.csv")
        dataSet = {}
        uniqueData =  df['pc'].unique()
        for unique in uniqueData:
            dataSet[unique] =  ",".join(df.loc[df['pc'] == unique,'address'])
        newCsv = pd.DataFrame(list(dataSet.iteritems()),columns=['pc', 'addresses'])
        newCsv.to_csv(fileLocation+"categorized_memory_w_profiling.csv")

        return True
    except Exception as e:
        logger.loggerError.debug("csv memory access mapping failed with Error : "+str(e))
        return False


def sharedMemoryMapping(fileName):
    global totalWindowNumber
    try:
        odf = pd.read_csv(fileLocation+"categorized_memory_fr_profiling.csv")
        resultDataSet = odf.to_dict(orient='records')
        for resultData in resultDataSet:
            subRowSet =  resultData['addresses'].split(',')
            tempLength = len(subRowSet)
            for i in range (0,int(math.ceil(len(subRowSet)/32.0))):
                if(tempLength>=32):
                    stride = 0
                    newLoop = True
                    changeStride = False
                    for j in range (i*32+1, (i+1)*32):
                        if(newLoop):
                            stride = abs(int(subRowSet[j].split('+')[0].split('x')[1],16)-int(subRowSet[j-1].split('+')[0].split('x')[1],16))
                            newLoop = False
                        else:
                            if (abs(int(subRowSet[j].split('+')[0].split('x')[1],16)-int(subRowSet[j-1].split('+')[0].split('x')[1],16)) == stride):
                                changeStride = False
                            else:
                                changeStride = True
                                break
                    totalWindowNumber = float(totalWindowNumber) +1

                    if not changeStride:
                        if((stride/4) % 2 == 1):
                            subProfileShMemBW["stride odd"] = subProfileShMemBW["stride odd"]+1
                        elif(stride/4 == 0):
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
                    tempLength = tempLength -32

        odf = pd.read_csv(fileLocation+"categorized_memory_sr_profiling.csv")
        resultDataSet = odf.to_dict(orient='records')
        for resultData in resultDataSet:
            subRowSet =  resultData['addresses'].split(',')
            tempLength = len(subRowSet)
            for i in range (0,int(math.ceil(len(subRowSet)/32.0))):
                if(tempLength>=32):
                    stride = 0
                    newLoop = True
                    changeStride = False
                    for j in range (i*32+1, (i+1)*32):
                        if(newLoop):
                            stride = abs(int(subRowSet[j].split('+')[0].split('x')[1],16)-int(subRowSet[j-1].split('+')[0].split('x')[1],16))
                            newLoop = False
                        else:
                            if (abs(int(subRowSet[j].split('+')[0].split('x')[1],16)-int(subRowSet[j-1].split('+')[0].split('x')[1],16)) == stride):
                                changeStride = False
                            else:
                                changeStride = True
                                break
                    totalWindowNumber = float(totalWindowNumber) +1

                    if not changeStride:
                        if((stride/4) % 2 == 1):
                            subProfileShMemBW["stride odd"] = subProfileShMemBW["stride odd"]+1
                        elif(stride/4 == 0):
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
                    tempLength = tempLength -32

        odf = pd.read_csv(fileLocation+"categorized_memory_w_profiling.csv")
        resultDataSet = odf.to_dict(orient='records')
        for resultData in resultDataSet:
            subRowSet =  resultData['addresses'].split(',')
            tempLength = len(subRowSet)
            for i in range (0,int(math.ceil(len(subRowSet)/32.0))):
                if(tempLength>=32):
                    stride = 0
                    newLoop = True
                    changeStride = False
                    for j in range (i*32+1, (i+1)*32):
                        if(newLoop):
                            stride = abs(int(subRowSet[j].split('+')[0].split('x')[1],16)-int(subRowSet[j-1].split('+')[0].split('x')[1],16))
                            newLoop = False
                        else:
                            if (abs(int(subRowSet[j].split('+')[0].split('x')[1],16)-int(subRowSet[j-1].split('+')[0].split('x')[1],16)) == stride):
                                changeStride = False
                            else:
                                changeStride = True
                                break
                    totalWindowNumber = float(totalWindowNumber) +1

                    if not changeStride:
                        if((stride/4) % 2 == 1):
                            subProfileShMemBW["stride odd"] = subProfileShMemBW["stride odd"]+1
                        elif(stride/4 == 0):
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
                    tempLength = tempLength -32

        noconf =  (int(subProfileShMemBW["stride odd"])/totalWindowNumber)
        totalCount = (int(subProfileShMemBW["stride odd"])/totalWindowNumber)+ ((int(subProfileShMemBW["stride 2"])/totalWindowNumber)/2.0)+ ((int(subProfileShMemBW["stride 4"])/totalWindowNumber)/4.0)+ ((int(subProfileShMemBW["stride 8"])/totalWindowNumber)/8.0)+ ((int(subProfileShMemBW["stride 16"])/totalWindowNumber)/16.0)+ (int((subProfileShMemBW["stride 32"])/totalWindowNumber)/32.0)
        broadCast = (int(subProfileShMemBW["broadCast"])/totalWindowNumber)
        text_file = open(fileLocation+"local_memory_stride.out", "w")
        text_file.write("noconf: "+str(noconf)+" totalCount: "+str(totalCount)+" broadCast: "+str(broadCast))
        text_file.close()
        return True
    except Exception as e:
        logger.loggerError.debug("sharedMemoryMapping extraction failed with Error : "+str(e))
        return False

def globalMemoryMapping(fileName):
    try:
        odf = pd.read_csv(fileLocation+"categorized_memory_fr_profiling.csv")
        resultDataSet = odf.to_dict(orient='records')
        for resultData in resultDataSet:
            subRowSet =  resultData['addresses'].split(',')
            tempLength = len(subRowSet)
            for i in range (0,int(math.ceil(len(subRowSet)/32.0))):
                if(tempLength>=32):
                    stride = 0
                    newLoop = True
                    changeStride = False
                    subArrayAddress = []
                    subArraySize = []
                    for j in range (i*32, (i+1)*32):
                        subArrayAddress.append(int(subRowSet[j].split('+')[0].split('x')[1],16))
                        subArraySize.append(int(subRowSet[j].split('+')[0].split('x')[1],16)+ int(subRowSet[j].split('+')[1].split('x')[1],16))
                    transactionCount = 0
                    while len(subArrayAddress)>0:
                        transactionCount = transactionCount + 1
                        subArrayAddress.sort()
                        subArraySize.sort()
                        tempCount = 0
                        for memItem in subArraySize:
                            if(memItem <= (subArrayAddress[0]+128)):
                                tempCount = tempCount +1
                            else:
                                break
                        del subArrayAddress[:tempCount]
                        del subArraySize[:tempCount]
                    subProfileGMemBW[transactionCount-1] = subProfileGMemBW[transactionCount-1]+1
                tempLength = tempLength -32

        odf = pd.read_csv(fileLocation+"categorized_memory_sr_profiling.csv")
        resultDataSet = odf.to_dict(orient='records')
        for resultData in resultDataSet:
            subRowSet =  resultData['addresses'].split(',')
            tempLength = len(subRowSet)
            for i in range (0,int(math.ceil(len(subRowSet)/32.0))):
                if(tempLength>=32):
                    stride = 0
                    newLoop = True
                    changeStride = False
                    subArrayAddress = []
                    subArraySize = []
                    for j in range (i*32, (i+1)*32):
                        subArrayAddress.append(int(subRowSet[j].split('+')[0].split('x')[1],16))
                        subArraySize.append(int(subRowSet[j].split('+')[0].split('x')[1],16)+ int(subRowSet[j].split('+')[1].split('x')[1],16))
                    transactionCount = 0
                    while len(subArrayAddress)>0:
                        transactionCount = transactionCount + 1
                        subArrayAddress.sort()
                        subArraySize.sort()
                        tempCount = 0
                        for memItem in subArraySize:
                            if(memItem <= (subArrayAddress[0]+128)):
                                tempCount = tempCount +1
                            else:
                                break
                        del subArrayAddress[:tempCount]
                        del subArraySize[:tempCount]
                    subProfileGMemBW[transactionCount-1] = subProfileGMemBW[transactionCount-1]+1
                tempLength = tempLength -32

        odf = pd.read_csv(fileLocation+"categorized_memory_w_profiling.csv")
        resultDataSet = odf.to_dict(orient='records')
        for resultData in resultDataSet:
            subRowSet =  resultData['addresses'].split(',')
            tempLength = len(subRowSet)
            for i in range (0,int(math.ceil(len(subRowSet)/32.0))):
                if(tempLength>=32):
                    stride = 0
                    newLoop = True
                    changeStride = False
                    subArrayAddress = []
                    subArraySize = []
                    for j in range (i*32, (i+1)*32):
                        subArrayAddress.append(int(subRowSet[j].split('+')[0].split('x')[1],16))
                        subArraySize.append(int(subRowSet[j].split('+')[0].split('x')[1],16)+ int(subRowSet[j].split('+')[1].split('x')[1],16))
                    transactionCount = 0
                    while len(subArrayAddress)>0:
                        transactionCount = transactionCount + 1
                        subArrayAddress.sort()
                        subArraySize.sort()
                        tempCount = 0
                        for memItem in subArraySize:
                            if(memItem <= (subArrayAddress[0]+128)):
                                tempCount = tempCount +1
                            else:
                                break
                        del subArrayAddress[:tempCount]
                        del subArraySize[:tempCount]
                    subProfileGMemBW[transactionCount-1] = subProfileGMemBW[transactionCount-1]+1
                tempLength = tempLength -32

        coalied = subProfileGMemBW[0]/totalWindowNumber
        totalTrans =0
        for index in range(0,32):
            totalTrans = totalTrans + (float(subProfileGMemBW[index])/totalWindowNumber)/float(index+1)
        text_file = open(fileLocation+"globle_memory_stride.out", "w")
        text_file.write("coalied: "+str(coalied)+" totalTrans: "+str(totalTrans))
        text_file.close()
        return True
    except Exception as e:
        print e
        logger.loggerError.debug("globalMemoryMapping extraction failed with Error : "+str(e))
        return False

# preMemoryMapping()
# sharedMemoryMapping()
# globalMemoryMapping()
