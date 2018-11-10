import logger,dbManager
from Vectorizer.Vectorizer import Vectorizer
from gpuMachineLearner.gpuMLExecuter import mlModelExecutor
from vecMachineLearner.vecMLExecuter import vecMlModelExecutor
from Modifier.occupanyCalculator.offloadOptimizer import runOffloadOptimizer
from Modifier.Scheduler.schedulerExecuter import schdedulerInitializer

response = {
    "returncode":0,
    "error":"",
    "content":{}
    }

def modify(extractor,directory):
    global response

    if(dbManager.read('gpuopt')) :
        logger.loggerInfo("Gpu Machine Learning Model Execution Initialized")
        result = mlModelExecutor(directory)
        if (result):
            logger.loggerSuccess("Gpu Machine Learning Model Execution Completed")
        else:
            logger.loggerError("Gpu Machine Learning Model Execution Failed. Gpu Optimizations will be skipped")
            dbManager.overWrite('gpuopt',False)



    if(dbManager.read('vecopt')) :
        logger.loggerInfo("Vector Machine Learning Model Execution Initialized")

        # result = vecMlModelExecutor(directory)
        # if (result):
        #     logger.loggerSuccess("Vec Machine Learning Model Execution Completed")
        # else:
        #     logger.loggerError("Vec Machine Learning Model Execution Failed.")


    # Database clean method

    if(dbManager.read('gpuopt')):
        logger.loggerInfo("GPU Optimization Initialized.")
        resultLocal = runOffloadOptimizer(extractor, directory)
        logger.loggerSuccess("GPU Optimization Completed.")


    if(dbManager.read('vecopt')) :
        logger.loggerInfo("Vector Optimization Initialized.")
        vectorizer = Vectorizer(extractor, directory)
        logger.loggerSuccess("Vector Optimization Completed")


    logger.loggerInfo("CPU Optimization Initialized")
    schdedulerInitializer(extractor, directory)
    logger.loggerSuccess("CPU Optimization Completed")

    return response
