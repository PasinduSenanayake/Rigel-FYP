from memoryDataFetcher import preMemoryMapping,sharedMemoryMapping,globalMemoryMapping
from branchingDataFetcher import preBranchDataFetch,fetchBranchInfo
from branchingFinalDataFetcher import finalBranchCounter
from collapseBranchingDataFetcher import preCollapseBranchDataFetch,fetchCollapseBranchInfo
from subprocess import Popen, PIPE
import re,os

fileLocation = os.path.dirname(os.path.realpath(__file__))+"/"

def runPinProf(loggerSuccess,loggerError,loggerInfo,arguments):
    resultPin = "success"
    loggerInfo.debug("ILP and instruction count extraction initiated")
    with open(fileLocation+'/mica.conf','w') as confFile:
        confFile.write("analysis_type: ilp\ninterval_size: full")
        confFile.close
    resultPin = profileInPin("mica.so",arguments)
    if(resultPin == "success"):
        loggerSuccess.debug("ILP and instruction count extraction completed")
        loggerInfo.debug("Operation count extraction initiated")
        with open(fileLocation+'/mica.conf','w') as confFile:
            confFile.write("analysis_type: itypes\ninterval_size: full")
            confFile.close
        resultPin = profileInPin("mica.so",arguments)
        if(resultPin == "success"):
            loggerSuccess.debug("Operation count extraction completed")
            loggerInfo.debug("Cold ref and reuse distance extraction initiated")
            with open(fileLocation+'/mica.conf','w') as confFile:
                confFile.write("analysis_type: memstackdist\ninterval_size: full\nblock_size: 7")
                confFile.close
            resultPin = profileInPin("mica.so",arguments)
            if(resultPin == "success"):
                loggerSuccess.debug("Cold ref and reuse distance extraction completed")
                loggerInfo.debug("Pages and Blocks extraction initiated")
                with open(fileLocation+'/mica.conf','w') as confFile:
                    confFile.write("analysis_type: memfootprint\ninterval_size: full\nblock_size: 7")
                    confFile.close
                resultPin = profileInPin("mica.so",arguments)
                if(resultPin == "success"):
                    loggerSuccess.debug("Pages and Blocks extraction completed")
                    loggerInfo.debug("Memory access extraction initiated")
                    resultPin = profileInPin("strides_count.so",arguments)
                    if(resultPin == "success"):
                        loggerSuccess.debug("Memory access extraction completed")
                        loggerInfo.debug("Memory access reordering initiated")
                        isCompleted = preMemoryMapping(loggerError)
                        if(isCompleted):
                            isCompleted = sharedMemoryMapping(loggerError)
                            if(isCompleted):
                                isCompleted = globalMemoryMapping(loggerError)
                                if not isCompleted:
                                    resultPin = "failed"
                            else:
                                resultPin = "failed"
                        else:
                            resultPin = "failed"
                        if(resultPin == "success"):
                            loggerSuccess.debug("Memory access reordering completed")
                            loggerInfo.debug("Branch info extraction initiated")
                            resultPin = profileInPin("branchFinder.so",arguments)
                            if(resultPin == "success"):
                                loggerSuccess.debug("Branch info extraction completed")
                                loggerInfo.debug("Branch info reordering initiated")
                                isCompleted = preBranchDataFetch(loggerError)
                                if(isCompleted):
                                    isCompleted = fetchBranchInfo(loggerError)
                                    if not isCompleted:
                                        resultPin = "failed"
                                else:
                                    resultPin = "failed"
                                if(resultPin == "success"):
                                    loggerSuccess.debug("Branch info reordering completed")
                                    loggerInfo.debug("Collapse Branch info extraction initiated")
                                    resultPin = profileTwoInPin("branchFinder.so",arguments)
                                    if(resultPin == "success"):
                                        loggerSuccess.debug("Collapse Branch info extraction completed")
                                        loggerInfo.debug("Collapse Branch info reordering initiated")
                                        isCompleted = preCollapseBranchDataFetch(loggerError)
                                        if(isCompleted):
                                            isCompleted = fetchCollapseBranchInfo(loggerError)
                                            if not isCompleted:
                                                resultPin = "failed"
                                        else:
                                            resultPin = "failed"
                                        if(resultPin == "success"):
                                            loggerSuccess.debug("Collapse Branch info reordering completed")
                                            loggerInfo.debug("Final Branch info reordering initiated")
                                            isCompleted = finalBranchCounter(loggerError)
                                            if not isCompleted:
                                                resultPin = "failed"
                                            if(resultPin == "success"):
                                                loggerSuccess.debug("Final Branch info reordering completed")
                                                loggerInfo.debug("Floating point info extraction initiated")
                                                resultPin = profileInPin("flop_counter.so",arguments)
                                                if(resultPin == "success"):
                                                    loggerSuccess.debug("Floating point info extraction completed")
                                                    loggerInfo.debug("Special function info extraction initiated")
                                                    resultPin = profileInPin("special_function_counter.so",arguments)
                                                    if not (resultPin == "success"):
                                                        loggerError.debug("Special function info extraction Failed Error: "+resultPin)
                                                else:
                                                    loggerError.debug("Floating point info extraction Failed Error: "+resultPin)
                                            else:
                                                loggerError.debug("Final Branch info reordering Failed")
                                        else:
                                            loggerError.debug("Collapse Branch info reordering Failed")
                                    else:
                                        loggerError.debug("Collapse Branch info extraction Failed Error: "+resultPin)
                                else:
                                    loggerError.debug("Branch info reordering Failed")
                            else:
                                loggerError.debug("Branch info extraction Failed Error: "+resultPin)
                        else:
                            loggerError.debug("Memory access reordering Failed")
                    else:
                        loggerError.debug("Memory access extraction Failed Error: "+resultPin)
                else:
                    loggerError.debug("Pages and Blocks extraction Failed Error: "+resultPin)
            else:
                loggerError.debug("Cold ref and reuse distance extraction Failed Error: "+resultPin)
        else:
            loggerError.debug("Operation count extraction Failed Error: "+resultPin)
    else:
        loggerError.debug("ILP and instruction count extraction Failed Error: "+resultPin)

    if(resultPin == "success"):
        return True
    else:
        return False

def profileInPin(soFile,arguments):
    executeString = 'cd '+fileLocation+' && ./pin -t '+soFile+' -- '+fileLocation+'runnable'
    processOutput = Popen(executeString,shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if error=="":
        return "success"
    elif "All done reading" in error:
        return "success"
    else:
        return error

def profileTwoInPin(soFile,arguments):
    executeString = 'cd '+fileLocation+' && ./pin -t '+soFile+' -- '+fileLocation+'runnableSecond'
    processOutput = Popen(executeString,shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if error=="":
        return "success"
    elif "All done reading" in error:
        return "success"
    else:
        return error
