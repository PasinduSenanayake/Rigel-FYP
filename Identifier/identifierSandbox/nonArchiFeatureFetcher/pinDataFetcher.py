
import os,csv


fileLocation = os.path.dirname(os.path.realpath(__file__))+"/"
dataRow =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


global tOps
global total_sp_float_ops

def dataCollect(loggerSuccess,loggerError,loggerInfo,csvPath):
    isCollectSuccess = True
    loggerInfo.debug("Check for new CSV")
    row_count = 0
    if not (os.path.isfile(csvPath)):
        with open(csvPath, 'w'): pass
    if(os.stat(csvPath).st_size == 0):
        loggerInfo.debug("Writing headers to CSV initiated")
        with open(csvPath, 'wb') as csvfile:
            inswriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            inswriter.writerow(['dataSet', 'instructionCount','ilp32','ilp256','ilp2048','ilp65536','memops','ctrlops','intops','flops','coldref','reuseDist2','sfp','dfp','noconflict','broadCast','coalesced','shMemBw','gMemBw','blocks','pages','lipRate','mulf','divf','specialFn','lbdiv16','lbdiv32','lbdiv64','lbdiv128','lbdiv256','lbdiv512','lbdiv1024'])
        loggerSuccess.debug("Writing headers to CSV completed")
        row_count = 1
    else:
        loggerInfo.debug("CSV contains previos data")
        with open(csvPath, 'r') as csvfile:
            row_count = sum(1 for row in csvfile)

    dataRow[0] = row_count

    loggerInfo.debug("Fetching ILP data initiated")
    if(os.path.isfile(fileLocation+'ilp_full_int_pin.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'ilp_full_int_pin.out','r')]
        separatedLines = lines[0].split(' ')
        dataRow[1]= int(separatedLines[0])
        dataRow[2]= float(separatedLines[0])/float(separatedLines[1])
        dataRow[3]= float(separatedLines[0])/float(separatedLines[2])
        dataRow[4]= float(separatedLines[0])/float(separatedLines[3])
        dataRow[5]= float(separatedLines[0])/float(separatedLines[4])
        loggerSuccess.debug("Fetching ILP data completed")
    else:
        isCollectSuccess = False
        loggerError.debug("Fetching ILP data failed")

    loggerInfo.debug("Fetching instructionType data initiated")
    if(os.path.isfile(fileLocation+'itypes_full_int_pin.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'itypes_full_int_pin.out','r')]
        loggerSuccess.debug("Fetching instructionType data completed")
    else:
        isCollectSuccess = False
        loggerError.debug("Fetching instructionType data failed")

    loggerInfo.debug("Fetching coldref and reuseDist data initiated")
    if(os.path.isfile(fileLocation+'memstackdist_full_int_pin.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'memstackdist_full_int_pin.out','r')]
        separatedLines = lines[0].split(' ')
        totalMemoryAccess = int(separatedLines[0])
        dataRow[10]= int(separatedLines[1])
        dataRow[11]= int(separatedLines[2])
        loggerSuccess.debug("Fetching coldref and reuseDist data completed")
    else:
        isCollectSuccess = False
        loggerError.debug("Fetching coldref and reuseDist data failed")

    loggerInfo.debug("Fetching pages and blocks data initiated")
    if(os.path.isfile(fileLocation+'memfootprint_full_int_pin.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'memfootprint_full_int_pin.out','r')]
        separatedLines = lines[0].split(' ')
        dataRow[19]= totalMemoryAccess/float(separatedLines[0])
        dataRow[20]= totalMemoryAccess/float(separatedLines[1])
        loggerSuccess.debug("Fetching pages and blocks data completed")
    else:
        isCollectSuccess = False
        loggerError.debug("Fetching pages and blocks data failed")

    loggerInfo.debug("Fetching global memory data initiated")
    if(os.path.isfile(fileLocation+'globle_memory_stride.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'globle_memory_stride.out','r')]
        globalMemoryData = lines[0].split(" ")
        dataRow[16]= float(globalMemoryData[1])
        dataRow[18]= float(globalMemoryData[3])
        loggerSuccess.debug("Fetching global memory data completed")
    else:
        isCollectSuccess = False
        loggerError.debug("Fetching global memory data failed")

    loggerInfo.debug("Fetching shared memory data initiated")
    if(os.path.isfile(fileLocation+'local_memory_stride.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'local_memory_stride.out','r')]
        sharedMemoryData = lines[0].split(" ")
        dataRow[14]= float(sharedMemoryData[1])
        dataRow[15]= float(sharedMemoryData[5])
        dataRow[17]= float(sharedMemoryData[3])
        loggerSuccess.debug("Fetching shared memory data completed")
    else:
        isCollectSuccess = False
        loggerError.debug("Fetching shared memory data failed")

    loggerInfo.debug("Featching Floating Point operation data initiated")

    if(os.path.isfile(fileLocation+'itypes_full_int_pin.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'itypes_full_int_pin.out','r')]
        totalOps =  lines[0].split(" ")
        memOps = int(totalOps[1])+int(totalOps[2])
        ctrlOps = int(totalOps[3])
        intOps = int(totalOps[4])
        global tOps
        tOps = int(totalOps[0])
        dataRow[6]= float(memOps)/float(tOps)
        dataRow[7]= float(ctrlOps)/float(tOps)
        dataRow[8]= float(intOps)/float(tOps)
        loggerSuccess.debug("Fetching shared memory data completed")
    else:
        isCollectSuccess = False
        loggerError.debug("Fetching shared memory data failed")

    loggerInfo.debug("Featching Floating Point operation data initiated")

    if(os.path.isfile(fileLocation+'flop_count.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'flop_count.out','r')]
        total_float_ops = lines[0].split(" ")[1]
        total_arith_float_ops = lines[1].split(" ")[1]
        global total_sp_float_ops
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
        loggerSuccess.debug("Featching Floating Point operation data completed")
    else:
        isCollectSuccess = False
        loggerError.debug("Featching Floating Point operation data failed")

    loggerInfo.debug("Featching Special Function data initiated")
    if(os.path.isfile(fileLocation+'special_func_count.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'special_func_count.out','r')]
        special_function_count = int(lines[0].split(" ")[1])
        dataRow[24] = float(special_function_count)/float(total_sp_float_ops)
        loggerSuccess.debug("Featching Special Function data completed")
    else:
        isCollectSuccess = False
        loggerError.debug("Featching Special Function data failed")

    loggerInfo.debug("Featching Branching data initiated")
    if(os.path.isfile(fileLocation+'branching_info.out')):
        lines = [line.rstrip('\n') for line in open(fileLocation+'branching_info.out','r')]
        dataRow[25] = float(lines[0].split(" ")[1])/float(tOps)
        dataRow[26] = float(lines[0].split(" ")[3])/float(tOps)
        dataRow[27] = float(lines[0].split(" ")[5])/float(tOps)
        dataRow[28] = float(lines[0].split(" ")[7])/float(tOps)
        dataRow[29] = float(lines[0].split(" ")[9])/float(tOps)
        dataRow[30] = float(lines[0].split(" ")[11])/float(tOps)
        dataRow[31] = float(lines[0].split(" ")[13])/float(tOps)
        loggerSuccess.debug("Featching Branching data completed")
    else:
        isCollectSuccess = False
        loggerError.debug("Featching Branching data failed")


    loggerInfo.debug("Writing to CSV initiated")
    with open(csvPath, 'a') as csvfile:
        inswriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        inswriter.writerow(dataRow)
    loggerSuccess.debug("Writing to CSV completed")

    return isCollectSuccess
