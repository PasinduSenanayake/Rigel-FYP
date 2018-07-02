# logging
import logging
import os
from shutil import copyfile
import shutil
from identifierSandbox.nonArchiFeatureFetcher.sourceAnnotator import targetDataMap
from identifierSandbox.nonArchiFeatureFetcher.collapsibleLoopAnnotator import collapseAnnotator
from identifierSandbox.nonArchiFeatureFetcher.pinProfilerExecutor import runPinProf
from identifierSandbox.nonArchiFeatureFetcher.pinDataFetcher import dataCollect


LOG_FILENAME = os.path.dirname(os.path.realpath(__file__))+"/nonArchiFeature.log"
logging.basicConfig(filename=LOG_FILENAME, filemode="w", level=logging.DEBUG)
loggerInfo = logging.getLogger("info:")
loggerError = logging.getLogger("error:")
loggerSuccess = logging.getLogger("success:")


def hotspotsProfiler(codeName,mainFilePath,annotatedFile,makeFile,compileCommand,arguments,segmentArray,initLocation):
    loggerInfo.debug("File coping started")
    isCopySuccessful = True
    subFilePath = ""
    if (os.path.isfile(mainFilePath)):
        subFilePath = mainFilePath.split("Sandbox")[1]
        makeFilePath = makeFile.split("Sandbox")[1]
        annotatedFilePath = annotatedFile.split("Sandbox")[1]
        if(os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/identifierSandbox/nonArchiFeatureFetcher/Sandbox")):
            shutil.rmtree(os.path.dirname(os.path.realpath(__file__))+"/identifierSandbox/nonArchiFeatureFetcher/Sandbox")
        shutil.copytree("./Sandbox", os.path.dirname(os.path.realpath(__file__))+"/identifierSandbox/nonArchiFeatureFetcher/Sandbox")
    else:
        loggerError.debug("No " + mainFilePath +" found. Process stopped" )
        isCopySuccessful = False
    if(isCopySuccessful):
        isprocessSuccesful = True
        loggerSuccess.debug("File coping completed")
        for segment in segmentArray:
            loggerInfo.debug("source code Annotation for "+str(segment[0])+"-"+str(segment[1])+" initiated")
            result = targetDataMap(annotatedFilePath,makeFilePath,compileCommand,segment[0],segment[1])
            if(result == "success"):
                loggerSuccess.debug("Source code Annotation for "+str(segment[0])+"-"+str(segment[1])+" completed")
                loggerInfo.debug("source code with collapse Annotation for "+str(segment[0])+"-"+str(segment[1])+" initiated")
                result = collapseAnnotator(annotatedFilePath,makeFilePath,compileCommand)
                if(result == "success"):
                    loggerSuccess.debug("Source code with collapse Annotation for "+str(segment[0])+"-"+str(segment[1])+" completed")
                    loggerInfo.debug("Pin profile for "+str(segment[0])+"-"+str(segment[1])+" initiated")
                    pinresult = runPinProf(loggerSuccess,loggerError,loggerInfo,arguments,subFilePath)
                    if(pinresult):
                        loggerSuccess.debug("Pin profile for "+str(segment[0])+"-"+str(segment[1])+" completed")
                        loggerInfo.debug("Information extraction for "+str(segment[0])+"-"+str(segment[1])+" initiated")
                        pinDataresult = dataCollect(codeName,str(segment[0]),str(segment[1]),loggerSuccess,loggerError,loggerInfo,initLocation+"/Benchmarks/machineLearning/gpuSuitability/gpuvscpu.csv",subFilePath)
                        if(pinDataresult):
                            loggerSuccess.debug("Data collect for "+str(segment[0])+"-"+str(segment[1])+" completed")
                        else:
                            loggerError.debug("Data collect for "+str(segment[0])+"-"+str(segment[1])+" failed")
                            isprocessSuccesful = False
                            break
                    else:
                        loggerError.debug("Pin profile for "+str(segment[0])+"-"+str(segment[1])+" failed")
                        isprocessSuccesful = False
                        break
                else:
                    loggerError.debug("Source code with collapse Annotation for "+str(segment[0])+"-"+str(segment[1])+" failed with Error : "+result)
                    isprocessSuccesful = False
                    break
            else:
                loggerError.debug("Source code Annotation for "+str(segment[0])+"-"+str(segment[1])+" failed with Error :: "+result)
                isprocessSuccesful = False
                break
        return isprocessSuccesful
    else:
        loggerError.debug("File coping failed")
        return False
