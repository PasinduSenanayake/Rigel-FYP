import logger,dbManager
from Vectorizer.Vectorizer import Vectorizer
from gpuMachineLearner.gpuMLExecuter import mlModelExecutor
from vecMachineLearner.vecMLExecuter import vecMlModelExecutor
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

    # result = vecMlModelExecutor(directory)
    # if (result):
    #     logger.loggerSuccess("Vec Machine Learning Model Execution Completed")
    # else:
    #     logger.loggerError("Vec Machine Learning Model Execution Failed.")

    # Database clean method

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

    # pragma = source.offload(vector["line"], "parallel for", 4, "map")
    # pragma.modifyClause("num_threads", 5)
    return response
