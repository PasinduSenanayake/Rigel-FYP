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
                        loggerInfo.debug("Branch info extraction initiated")
                        resultPin = profileInPin("branchFinder.so",arguments)
                        if(resultPin == "success"):
                            loggerSuccess.debug("Branch info extraction completed")
                        else:
                            loggerError.debug("Branch info extraction Failed")
                    else:
                        loggerError.debug("Memory access extraction Failed")
                else:
                    loggerError.debug("Pages and Blocks extraction Failed")
            else:
                loggerError.debug("Cold ref and reuse distance extraction Failed")
        else:
            loggerError.debug("Operation count extraction Failed")
    else:
        loggerError.debug("ILP and instruction count extraction Failed")

    if(resultPin == "success"):
        return True
    else:
        return False

def profileInPin(soFile,arguments):
    executeString = 'cd '+fileLocation+' && ./pin -t '+soFile+' -- '+fileLocation+'runnable'
    processOutput = Popen(executeString,shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    print error
    if error=="":
        return "success"
    elif "All done reading" in error:
        return "success"
    else:
        return error
