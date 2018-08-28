# logging
import logger
import os
from shutil import copyfile
import shutil
from identifierSandbox.nonArchiFeatureFetcher.sourceAnnotator import targetDataMap
from identifierSandbox.nonArchiFeatureFetcher.sourceAnnotatorILP import targetDataMapILP
from identifierSandbox.nonArchiFeatureFetcher.sourceAnnotatorBranch import targetDataMapBranch
from identifierSandbox.nonArchiFeatureFetcher.collapsibleLoopAnnotator import collapseAnnotator
from identifierSandbox.nonArchiFeatureFetcher.pinProfilerExecutor import runPinProf
from identifierSandbox.nonArchiFeatureFetcher.pinDataFetcher import dataCollect



def hotspotsProfiler(codeName,mainFilePath,annotatedFile,makeFile,compileCommand,arguments,segmentArray,initLocation):
    logger.loggerInfo("File coping started")
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
        logger.loggerError("No " + mainFilePath +" found. Process stopped" )
        isCopySuccessful = False
    if(isCopySuccessful):
        isprocessSuccesful = True
        logger.loggerSuccess("File coping completed")
        for segment in segmentArray:
            logger.loggerInfo("source code Annotation for "+str(segment[0])+"-"+str(segment[1])+" initiated")
            result = targetDataMap(annotatedFilePath,makeFilePath,compileCommand,segment[0],segment[1])
            if(result == "success"):
                logger.loggerSuccess("Source code Annotation for "+str(segment[0])+"-"+str(segment[1])+" completed")
                logger.loggerInfo("source code with ILP Annotation for "+str(segment[0])+"-"+str(segment[1])+" initiated")
                result = targetDataMapILP(annotatedFilePath,makeFilePath,compileCommand,segment[0],segment[1])
                if(result == "success"):
                    logger.loggerSuccess("Source code with ILP Annotation for "+str(segment[0])+"-"+str(segment[1])+" completed")
                    logger.loggerInfo("source code with branch Annotation for "+str(segment[0])+"-"+str(segment[1])+" initiated")
                    result = targetDataMapBranch(annotatedFilePath,makeFilePath,compileCommand,segment[0],segment[1])
                    if(result == "success"):
                        logger.loggerSuccess("Source code with branch Annotation for "+str(segment[0])+"-"+str(segment[1])+" completed")
                        logger.loggerInfo("source code with collapse Annotation for "+str(segment[0])+"-"+str(segment[1])+" initiated")
                        result = collapseAnnotator(annotatedFilePath,makeFilePath,compileCommand)
                        if(result == "success"):
                            logger.loggerSuccess("Source code with collapse Annotation for "+str(segment[0])+"-"+str(segment[1])+" completed")
                            logger.loggerInfo("Pin profile for "+str(segment[0])+"-"+str(segment[1])+" initiated")
                            pinresult = runPinProf(arguments,subFilePath)
                            if(pinresult):
                                logger.loggerSuccess("Pin profile for "+str(segment[0])+"-"+str(segment[1])+" completed")
                                logger.loggerInfo("Information extraction for "+str(segment[0])+"-"+str(segment[1])+" initiated")
                                pinDataresult = dataCollect(codeName,str(segment[0]),str(segment[1]),initLocation+"/Benchmarks/machineLearning/gpuSuitability/gpuvscpu.csv",subFilePath)
                                if(pinDataresult):
                                    logger.loggerSuccess("Data collect for "+str(segment[0])+"-"+str(segment[1])+" completed")
                                else:
                                    logger.loggerError("Data collect for "+str(segment[0])+"-"+str(segment[1])+" failed")
                                    isprocessSuccesful = False
                                    break
                            else:
                                logger.loggerError("Pin profile for "+str(segment[0])+"-"+str(segment[1])+" failed")
                                isprocessSuccesful = False
                                break
                        else:
                            logger.loggerError("Source code with collapse Annotation for "+str(segment[0])+"-"+str(segment[1])+" failed with Error : "+result)
                            isprocessSuccesful = False
                            break
                    else:
                        logger.loggerError("Source code with branch Annotation for "+str(segment[0])+"-"+str(segment[1])+" failed with Error : "+result)
                        isprocessSuccesful = False
                        break
                else:
                    logger.loggerError("Source code with ILP Annotation for "+str(segment[0])+"-"+str(segment[1])+" failed with Error : "+result)
                    isprocessSuccesful = False
                    break
            else:
                logger.loggerError("Source code Annotation for "+str(segment[0])+"-"+str(segment[1])+" failed with Error :: "+result)
                isprocessSuccesful = False
                break
        return isprocessSuccesful
    else:
        logger.loggerError("File coping failed")
        return False
