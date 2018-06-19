# logging
import logging
import os
from shutil import copyfile
from identifierSandbox.nonArchiFeatureFetcher.sourceAnnotator import targetDataMap
from identifierSandbox.nonArchiFeatureFetcher.pinProfilerExecutor import runPinProf

profilingSet = {
    "instructionCount" : {"profFile":"ins"}
}

LOG_FILENAME = os.path.dirname(os.path.realpath(__file__))+"/nonArchiFeature.log"
logging.basicConfig(filename=LOG_FILENAME, filemode="w", level=logging.DEBUG)
loggerInfo = logging.getLogger("info:")
loggerError = logging.getLogger("error:")
loggerSuccess = logging.getLogger("success:")
# logger.debug("hiho debug message")


def hotspotsProfiler(mainFilePath,subFilesPath,compileCommand,arguments,segmentArray):
    loggerInfo.debug("File coping started")
    isCopySuccessful = True
    if (os.path.isfile(mainFilePath)):
        copyfile(mainFilePath, os.path.dirname(os.path.realpath(__file__))+"/identifierSandbox/nonArchiFeatureFetcher/profileCode.c")
    else:
        loggerError.debug("No " + mainFilePath +" found. Process stopped" )
        isCopySuccessful = False
    if(isCopySuccessful):
        for fileName in subFilesPath:
            if (os.path.isfile(fileName)):
                copyfile(fileName, os.path.dirname(os.path.realpath(__file__))+"/identifierSandbox/nonArchiFeatureFetcher/"+os.path.basename(fileName))
            else:
                loggerError.debug("No " + fileName +" found. Process stopped")
                isCopySuccessful = False
                break
    if(isCopySuccessful):
        loggerSuccess.debug("File coping completed")
        for segment in segmentArray:
            loggerInfo.debug("source code Annotation for "+str(segment[0])+"-"+str(segment[1])+" initiated")
            result = targetDataMap("profileCode.c",compileCommand,segment[0],segment[1])
            if(result == "success"):
                loggerSuccess.debug("Source code Annotation for "+str(segment[0])+"-"+str(segment[1])+" completed")
                loggerInfo.debug("Pin profile for "+str(segment[0])+"-"+str(segment[1])+" initiated")
                pinresult = runPinProf(loggerSuccess,loggerError,loggerInfo,arguments)
                if(pinresult):
                    loggerSuccess.debug("Pin profile for "+str(segment[0])+"-"+str(segment[1])+" completed")
                    loggerInfo.debug("Information extraction for "+str(segment[0])+"-"+str(segment[1])+" initiated")

                else:
                    loggerError.debug("Pin profile for "+str(segment[0])+"-"+str(segment[1])+" failed")
                    isCopySuccessful = False
                    break
            else:
                loggerError.debug("Source code Annotation for "+str(segment[0])+"-"+str(segment[1])+" failed with Error :: "+result)





            #execute profiler
