
import os,csv
import logger



fileLocation = os.path.dirname(os.path.realpath(__file__))+"/Sandbox"
dataRow =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


tOps = 0
total_sp_float_ops = 0

def dataCollect(codeName,initLine,endLine,csvPath,fileName):
    global fileLocation
    global tOps
    global total_sp_float_ops

    fileLocation = fileLocation+fileName.rsplit('/', 1)[0]+"/"
    isCollectSuccess = True
    logger.loggerInfo("Check for new CSV")
    row_count = 0
    if not (os.path.isfile(csvPath)):
        with open(csvPath, 'w'): pass
    if(os.stat(csvPath).st_size == 0):
        logger.loggerInfo("Writing headers to CSV initiated")
        with open(csvPath, 'wb') as csvfile:
            inswriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            inswriter.writerow(['dataSet', 'instructionCount','ilp32','ilp256','ilp2048','ilp65536','memops','ctrlops','intops','flops','coldref','reuseDist2','sfp','dfp','noconflict','broadCast','coalesced','shMemBw','gMemBw','blocks','pages','lipRate','mulf','divf','specialFn','lbdiv16','lbdiv32','lbdiv64','lbdiv128','lbdiv256','lbdiv512','lbdiv1024','probsize'])
        logger.loggerSuccess("Writing headers to CSV completed")
        row_count = 1
    else:
        logger.loggerInfo("CSV contains previos data")
        with open(csvPath, 'r') as csvfile:
            row_count = sum(1 for row in csvfile)

    dataRow[0] = str(row_count)+". "+codeName+': '+initLine+'-'+endLine

    logger.loggerInfo("Fetching ILP data initiated")
    if(os.path.isfile(fileLocation+'ilp_full_int_pin.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'ilp_full_int_pin.out','r')]
        separatedLines = lines[0].split(' ')
        for ite in range (1,6):
            if(separatedLines[ite]=='0'):
                separatedLines[ite]='1'
        if(os.path.isfile(fileLocation+'itypes_full_int_pin.out')):
            lines = [line.rstrip('\n') for line in open(fileLocation+'itypes_full_int_pin.out','r')]
            totalOperations =  lines[0].split(" ")
        dataRow[1]= int(totalOperations[0])
        dataRow[2]= float(separatedLines[0])/float(separatedLines[1])
        dataRow[3]= float(separatedLines[0])/float(separatedLines[2])
        dataRow[4]= float(separatedLines[0])/float(separatedLines[3])
        dataRow[5]= float(separatedLines[0])/float(separatedLines[5])
        dataRow[21]= float(separatedLines[4])/float(separatedLines[1])
        dataRow[32] = int(totalOperations[0])/int(separatedLines[0])
        logger.loggerSuccess("Fetching ILP data completed")
    else:
        isCollectSuccess = False
        logger.loggerError("Fetching ILP data failed")

    logger.loggerInfo("Fetching instructionType data initiated")
    if(os.path.isfile(fileLocation+'itypes_full_int_pin.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'itypes_full_int_pin.out','r')]
        logger.loggerSuccess("Fetching instructionType data completed")
    else:
        isCollectSuccess = False
        logger.loggerError("Fetching instructionType data failed")

    logger.loggerInfo("Fetching coldref and reuseDist data initiated")
    if(os.path.isfile(fileLocation+'memstackdist_full_int_pin.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'memstackdist_full_int_pin.out','r')]
        separatedLines = lines[0].split(' ')
        totalMemoryAccess = int(separatedLines[0])
        dataRow[10]= int(separatedLines[1])
        dataRow[11]= int(separatedLines[2])
        logger.loggerSuccess("Fetching coldref and reuseDist data completed")
    else:
        isCollectSuccess = False
        logger.loggerError("Fetching coldref and reuseDist data failed")

    logger.loggerInfo("Fetching pages and blocks data initiated")
    if(os.path.isfile(fileLocation+'memfootprint_full_int_pin.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'memfootprint_full_int_pin.out','r')]
        separatedLines = lines[0].split(' ')
        dataRow[19]= totalMemoryAccess/float(separatedLines[0])
        dataRow[20]= totalMemoryAccess/float(separatedLines[1])
        logger.loggerSuccess("Fetching pages and blocks data completed")
    else:
        isCollectSuccess = False
        logger.loggerError("Fetching pages and blocks data failed")

    logger.loggerInfo("Fetching global memory data initiated")
    if(os.path.isfile(fileLocation+'globle_memory_stride.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'globle_memory_stride.out','r')]
        globalMemoryData = lines[0].split(" ")
        dataRow[16]= float(globalMemoryData[1])
        dataRow[18]= float(globalMemoryData[3])
        logger.loggerSuccess("Fetching global memory data completed")
    else:
        isCollectSuccess = False
        logger.loggerError("Fetching global memory data failed")

    logger.loggerInfo("Fetching shared memory data initiated")
    if(os.path.isfile(fileLocation+'local_memory_stride.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'local_memory_stride.out','r')]
        sharedMemoryData = lines[0].split(" ")
        dataRow[14]= float(sharedMemoryData[1])
        dataRow[15]= float(sharedMemoryData[5])
        dataRow[17]= float(sharedMemoryData[3])
        logger.loggerSuccess("Fetching shared memory data completed")
    else:
        isCollectSuccess = False
        logger.loggerError("Fetching shared memory data failed")

    logger.loggerInfo("Featching Floating Point operation data initiated")

    if(os.path.isfile(fileLocation+'itypes_full_int_pin.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'itypes_full_int_pin.out','r')]
        totalOps =  lines[0].split(" ")
        memOps = int(totalOps[1])+int(totalOps[2])
        ctrlOps = int(totalOps[3])
        intOps = int(totalOps[4])
        tOps = int(totalOps[0])
        dataRow[6]= float(memOps)/float(tOps)
        dataRow[7]= float(ctrlOps)/float(tOps)
        dataRow[8]= float(intOps)/float(tOps)
        logger.loggerSuccess("Fetching shared memory data completed")
    else:
        isCollectSuccess = False
        logger.loggerError("Fetching shared memory data failed")

    logger.loggerInfo("Featching Floating Point operation data initiated")

    if(os.path.isfile(fileLocation+'flop_count.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'flop_count.out','r')]
        total_float_ops = lines[0].split(" ")[1]
        total_arith_float_ops = lines[1].split(" ")[1]
        total_sp_float_ops = lines[2].split(" ")[1]
        total_arith_sp_float_ops = lines[3].split(" ")[1]
        total_dp_float_ops = lines[4].split(" ")[1]
        total_arith_dp_float_ops = lines[5].split(" ")[1]
        total_sp_mul_float_ops = lines[6].split(" ")[1]
        total_sp_div_float_ops = lines[7].split(" ")[1]

        dataRow[12]= float(total_arith_sp_float_ops)/float(total_float_ops)
        dataRow[13]= float(total_arith_dp_float_ops)/float(total_float_ops)
        dataRow[9]= float(total_float_ops)/float(tOps)
        dataRow[22]= float(total_sp_mul_float_ops)/float(total_sp_float_ops)
        dataRow[23]= float(total_sp_div_float_ops)/float(total_sp_float_ops)
        logger.loggerSuccess("Featching Floating Point operation data completed")
    else:
        isCollectSuccess = False
        logger.loggerError("Featching Floating Point operation data failed")

    logger.loggerInfo("Featching Special Function data initiated")
    if(os.path.isfile(fileLocation+'special_func_count.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'special_func_count.out','r')]
        special_function_count = int(lines[0].split(" ")[1])
        dataRow[24] = float(special_function_count)/float(total_sp_float_ops)
        logger.loggerSuccess("Featching Special Function data completed")
    else:
        isCollectSuccess = False
        logger.loggerError("Featching Special Function data failed")

    logger.loggerInfo("Featching Branching data initiated")
    if(os.path.isfile(fileLocation+'branching_info.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'branching_info.out','r')]
        dataRow[25] = float(lines[0].split(" ")[1])/float(tOps)
        dataRow[26] = float(lines[0].split(" ")[3])/float(tOps)
        dataRow[27] = float(lines[0].split(" ")[5])/float(tOps)
        dataRow[28] = float(lines[0].split(" ")[7])/float(tOps)
        dataRow[29] = float(lines[0].split(" ")[9])/float(tOps)
        dataRow[30] = float(lines[0].split(" ")[11])/float(tOps)
        dataRow[31] = float(lines[0].split(" ")[13])/float(tOps)
        logger.loggerSuccess("Featching Branching data completed")
    else:
        isCollectSuccess = False
        logger.loggerError("Featching Branching data failed")


    logger.loggerInfo("Writing to CSV initiated")
    with open(csvPath, 'a') as csvfile:
        inswriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        inswriter.writerow(dataRow)
    logger.loggerSuccess("Writing to CSV completed")

    return isCollectSuccess
