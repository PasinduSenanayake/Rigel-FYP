from memoryDataFetcher import preMemoryMapping,sharedMemoryMapping,globalMemoryMapping
from branchingDataFetcher import preBranchDataFetch,fetchBranchInfo
from branchingFinalDataFetcher import finalBranchCounter
from collapseBranchingDataFetcher import preCollapseBranchDataFetch,fetchCollapseBranchInfo
from subprocess import Popen, PIPE
import re,os,logger

fileLocation = os.path.dirname(os.path.realpath(__file__))+"/"
baseFileLocation = os.path.dirname(os.path.realpath(__file__))+"/Sandbox"

def runPinProf(arguments,filePath):
    global baseFileLocation
    baseFileLocation = baseFileLocation+filePath.rsplit('/', 1)[0]
    resultPin = "success"
    logger.loggerInfo("ILP and extraction initiated")
    with open(baseFileLocation+'/mica.conf','w') as confFile:
        confFile.write("analysis_type: ilp\ninterval_size: full")
        confFile.close
    resultPin = profileILPInPin("mica.so",arguments)
    if(resultPin == "success"):
        logger.loggerSuccess("ILP extraction completed")
        logger.loggerInfo("Operation count extraction initiated")
        with open(baseFileLocation+'/mica.conf','w') as confFile:
            confFile.write("analysis_type: itypes\ninterval_size: full")
            confFile.close
        resultPin = profileInPin("mica.so",arguments)
        if(resultPin == "success"):
            logger.loggerSuccess("Operation count extraction completed")
            logger.loggerInfo("Cold ref and reuse distance extraction initiated")
            with open(baseFileLocation+'/mica.conf','w') as confFile:
                confFile.write("analysis_type: memstackdist\ninterval_size: full\nblock_size: 7")
                confFile.close
            resultPin = profileInPin("mica.so",arguments)
            if(resultPin == "success"):
                logger.loggerSuccess("Cold ref and reuse distance extraction completed")
                logger.loggerInfo("Pages and Blocks extraction initiated")
                with open(baseFileLocation+'/mica.conf','w') as confFile:
                    confFile.write("analysis_type: memfootprint\ninterval_size: full\nblock_size: 7")
                    confFile.close
                resultPin = profileInPin("mica.so",arguments)
                if(resultPin == "success"):
                    logger.loggerSuccess("Pages and Blocks extraction completed")
                    logger.loggerInfo("Memory access extraction initiated")
                    resultPin = profileInPin("strides_count.so",arguments)
                    if(resultPin == "success"):
                        logger.loggerSuccess("Memory access extraction completed")
                        logger.loggerInfo("Memory access reordering initiated")
                        isCompleted = preMemoryMapping(filePath)
                        if(isCompleted):
                            isCompleted = sharedMemoryMapping(filePath)
                            if(isCompleted):
                                isCompleted = globalMemoryMapping(filePath)
                                if not isCompleted:
                                    resultPin = "failed"
                            else:
                                resultPin = "failed"
                        else:
                            resultPin = "failed"
                        if(resultPin == "success"):
                            logger.loggerSuccess("Memory access reordering completed")
                            logger.loggerInfo("Branch info extraction initiated")
                            resultPin = profileBranchInPin("branchFinder.so",arguments)
                            if(resultPin == "success"):
                                logger.loggerSuccess("Branch info extraction completed")
                                logger.loggerInfo("Branch info reordering initiated")
                                isCompleted = fetchBranchInfo(filePath)
                                if not isCompleted:
                                    resultPin = "failed"

                                # isCompleted = preBranchDataFetch(filePath)
                                # if(isCompleted):
                                #     isCompleted = fetchBranchInfo()
                                #     if not isCompleted:
                                #         resultPin = "failed"
                                # else:
                                #     resultPin = "failed"
                                if(resultPin == "success"):
                                    logger.loggerSuccess("Branch info reordering completed")
                                    logger.loggerInfo("Collapse Branch info extraction initiated")
                                    resultPin = profileTwoInPin("branchFinder.so",arguments)
                                    if(resultPin == "success"):
                                        logger.loggerSuccess("Collapse Branch info extraction completed")
                                        logger.loggerInfo("Collapse Branch info reordering initiated")
                                        isCompleted = fetchCollapseBranchInfo(filePath)
                                        if not isCompleted:
                                            resultPin = "failed"
                                        # isCompleted = preCollapseBranchDataFetch(filePath)
                                        # if(isCompleted):
                                        #     isCompleted = fetchCollapseBranchInfo()
                                        #     if not isCompleted:
                                        #         resultPin = "failed"
                                        # else:
                                        #     resultPin = "failed"
                                        if(resultPin == "success"):
                                            logger.loggerSuccess("Collapse Branch info reordering completed")
                                            logger.loggerInfo("Final Branch info reordering initiated")
                                            isCompleted = finalBranchCounter(filePath)
                                            if not isCompleted:
                                                resultPin = "failed"
                                            if(resultPin == "success"):
                                                logger.loggerSuccess("Final Branch info reordering completed")
                                                logger.loggerInfo("Floating point info extraction initiated")
                                                resultPin = profileInPin("flop_counter.so",arguments)
                                                if(resultPin == "success"):
                                                    logger.loggerSuccess("Floating point info extraction completed")
                                                    logger.loggerInfo("Special function info extraction initiated")
                                                    resultPin = profileInPin("special_function_counter.so",arguments)
                                                    if not (resultPin == "success"):
                                                        logger.loggerError("Special function info extraction Failed Error: "+resultPin)
                                                else:
                                                    logger.loggerError("Floating point info extraction Failed Error: "+resultPin)
                                            else:
                                                logger.loggerError("Final Branch info reordering Failed")
                                        else:
                                            logger.loggerError("Collapse Branch info reordering Failed")
                                    else:
                                        logger.loggerError("Collapse Branch info extraction Failed Error: "+resultPin)
                                else:
                                    logger.loggerError("Branch info reordering Failed")
                            else:
                                logger.loggerError("Branch info extraction Failed Error: "+resultPin)
                        else:
                            logger.loggerError("Memory access reordering Failed")
                    else:
                        logger.loggerError("Memory access extraction Failed Error: "+resultPin)
                else:
                    logger.loggerError("Pages and Blocks extraction Failed Error: "+resultPin)
            else:
                logger.loggerError("Cold ref and reuse distance extraction Failed Error: "+resultPin)
        else:
            logger.loggerError("Operation count extraction Failed Error: "+resultPin)
    else:
        logger.loggerError("ILP  extraction Failed Error: "+resultPin)


    if(resultPin == "success"):
        return True
    else:
        return False

def profileInPin(soFile,arguments):
    executeString = 'cd '+baseFileLocation +' && '+fileLocation+'pin -t '+fileLocation+''+soFile+' -- '+baseFileLocation+'/runnable'+" "+arguments
    processOutput = Popen(executeString,shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if error=="":
        return "success"
    elif "All done reading" in error:
        return "success"
    elif "getcwd()" in error:
        return "success"
    else:
        return error

def profileTwoInPin(soFile,arguments):
    executeString = 'cd '+baseFileLocation +' && '+fileLocation+'pin -t '+fileLocation+''+soFile+' -- '+baseFileLocation+'/runnableSecond'+" "+arguments
    processOutput = Popen(executeString,shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if error=="":
        return "success"
    elif "All done reading" in error:
        return "success"
    elif "getcwd()" in error:
        return "success"
    else:
        return error

def profileILPInPin(soFile,arguments):
    executeString = 'cd '+baseFileLocation +' && '+fileLocation+'pin -t '+fileLocation+''+soFile+' -- '+baseFileLocation+'/runnableILP'+" "+arguments
    processOutput = Popen(executeString,shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if error=="":
        return "success"
    elif "All done reading" in error:
        return "success"
    elif "getcwd()" in error:
        return "success"
    else:
        return error


def profileBranchInPin(soFile,arguments):
    executeString = 'cd '+baseFileLocation +' && '+fileLocation+'pin -t '+fileLocation+''+soFile+' -- '+baseFileLocation+'/runnableBranch'+" "+arguments
    processOutput = Popen(executeString,shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if error=="":
        return "success"
    elif "All done reading" in error:
        return "success"
    elif "getcwd()" in error:
        return "success"
    else:
        return error
