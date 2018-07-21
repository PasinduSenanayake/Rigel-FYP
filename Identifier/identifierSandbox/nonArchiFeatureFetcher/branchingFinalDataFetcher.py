
import json,os,logger


fileLocation = os.path.dirname(os.path.realpath(__file__))+"/Sandbox"
finalCount = [0,0,0,0,0,0,0]
iterations = ['16','32','64','128','256','512','1024']



def finalBranchCounter(fileName):
    global fileLocation
    fileLocation = fileLocation+fileName.rsplit('/', 1)[0]+"/"
    try:
        with open(fileLocation+"branching.json", "r") as fin:
            mainData = json.load(fin)

        with open(fileLocation+"branching_collapse.json", "r") as fin:
            subData = json.load(fin)

        for index,ite in enumerate(iterations):
            mainTotal = 0
            subTotal = 0
            for mainSingleData in mainData:
                mainTotal = mainTotal+ (float(mainSingleData[ite]['ratio'])*float(mainSingleData[ite]["size"]))
            for subSingleData in subData:
                subTotal = subTotal+ (float(subSingleData[ite]['ratio'])*float(subSingleData[ite]["size"]))
            finalCount[index] = mainTotal - subTotal
        text_file = open(fileLocation+"branching_info.out", "w")
        text_file.write("16: "+str(finalCount[0])+" 32: "+str(finalCount[1])+" 64: "+str(finalCount[2])+" 128: "+str(finalCount[3])+" 256: "+str(finalCount[4])+" 512: "+str(finalCount[5])+" 1024: "+str(finalCount[6]))
        text_file.close()
        return True
    except Exception as e:
        logger.loggerError.debug("Final Branch count failed with Error : "+str(e))
        return False
