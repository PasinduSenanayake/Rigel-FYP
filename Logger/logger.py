import logging
import inspect,os,datetime


loggerInfoData = None
loggerErrorData = None
loggerSuccessData = None

def createLog():
    global loggerInfoData,loggerErrorData,loggerSuccessData
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    fileName = module.__file__

    if fileName == "Initializer.py":
        LOG_FILENAME = os.path.dirname(os.path.realpath(__file__))+"/logfiles/"+str(datetime.datetime.now())+"_process.log"
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',filename=LOG_FILENAME, filemode="w", level=logging.DEBUG)
        loggerInfoData = logging.getLogger("info:")
        loggerErrorData = logging.getLogger("error:")
        loggerSuccessData = logging.getLogger("success:")

    if fileName == "subCommandExecuter.py":
        LOG_FILENAME = os.path.dirname(os.path.realpath(__file__))+"/logfiles/"+str(datetime.datetime.now())+"_command_process.log"
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',filename=LOG_FILENAME, filemode="w", level=logging.DEBUG)
        loggerInfoData = logging.getLogger("info:")
        loggerErrorData = logging.getLogger("error:")
        loggerSuccessData = logging.getLogger("success:")


def loggerInfo(message):
    if not loggerInfoData == None:
        loggerInfoData.debug(message)
    else:
        print "Please initiate a log file."
        exit()

def loggerError(message):
    if not loggerErrorData == None:
        loggerErrorData.debug(message)
    else:
        print "Please initiate a log file."
        exit()

def loggerSuccess(message):
    if not loggerSuccessData == None:
        loggerSuccessData.debug(message)
    else:
        print "Please initiate a log file."
        exit()
