import logger
from Vectorizer.Vectorizer import Vectorizer
from gpuMachineLearner.gpuMLExecuter import mlModelExecutor

response = {
    "returncode":0,
    "error":"",
    "content":{}
    }

def modify(extractor,directory):
    global response
    logger.loggerInfo("Gpu Machine Learning Model Execution Initialized")
    result = mlModelExecutor(directory)
    if (result):
        logger.loggerSuccess("Gpu Machine Learning Model Execution Completed")
    else:
        logger.loggerError("Gpu Machine Learning Model Execution Terminated.")
    exit()

    logger.loggerInfo("Vector Machine Learning Model Execution Initialized")
    # mlModelExecutor(filePath)
    logger.loggerSuccess("Vector Machine Learning Model Execution Completed")

    vectorizer = Vectorizer(extractor, directory)

    # pragma = source.offload(vector["line"], "parallel for", 4, "map")
    # pragma.modifyClause("num_threads", 5)
    return response
