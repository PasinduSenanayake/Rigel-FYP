import logger,dbManager
from Vectorizer.Vectorizer import Vectorizer
from gpuMachineLearner.gpuMLExecuter import mlModelExecutor
from Modifier.occupanyCalculator.offloadOptimizer import runOffloadOptimizer

response = {
    "returncode":0,
    "error":"",
    "content":{}
    }

def modify(extractor,directory):
    global response
    logger.loggerInfo("Gpu Machine Learning Model Execution Initialized")

    # result = mlModelExecutor(directory)
    # if (result):
    #     logger.loggerSuccess("Gpu Machine Learning Model Execution Completed")
    # else:
    #     logger.loggerError("Gpu Machine Learning Model Execution Failed.")

    logger.loggerInfo("Vector Machine Learning Model Execution Initialized")

    logger.loggerSuccess("Vector Machine Learning Model Execution Completed")

    logger.loggerInfo("GPU Optimization Initialized.")

    resultLocal = runOffloadOptimizer(extractor, directory)

    logger.loggerSuccess("GPU Optimization Completed.")

    print dbManager.read('summaryLoops')
    print dbManager.read('GPU_OptTime')

    exit()

    logger.loggerInfo("Vector Optimization Initialized.")

    vectorizer = Vectorizer(extractor, directory)

    logger.loggerSuccess("Vector Optimization Completed")

    logger.loggerInfo("CPU Optimization Initialized")

    logger.loggerSuccess("CPU Optimization Completed")

    return response
