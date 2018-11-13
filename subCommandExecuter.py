import json,os,sys
import shutil
import random
import copy

sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Logger")
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/DatabaseManager")
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Utils")
import dbManager,logger
from Identifier.vectorFeatureFetcher import vecAnalzyer
from Modifier.Vectorizer.Vectorizer import Vectorizer
from Identifier.nonarchiFeatureFetcher import hotspotsProfiler
from Modifier.occupanyCalculator.offloadChecker import occupancyCalculation
from Modifier.Scheduler.schedulerExecuter import schdedulerInitializer
from Modifier.gpuMachineLearner.gpuMLExecuter import mlModelExecutor
from Modifier.vecMachineLearner.vecMLExecuter import vecMlModelExecutor
from Identifier.identifierSandbox.sourceCodeAnnotation.sourceAnnotator import targetDataMap
from Modifier.modifierSandbox.arrayInfoIdentifier.arrayInfoFetcher import arrayInfoFetch
from Modifier.occupanyCalculator.offloadOptimizer import runOffloadOptimizer
from Identifier.summaryIdentifier.initilizerOmpp import getSummary
from Identifier.systemIdentifier.systemIdentifier import __systemInformationIdentifier
from Evaluator.visualizer import reportGenerator

if(os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json")):
    with open(os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json") as f:
        commandJson = json.load(f)

result = {
    'code':0,
    'content':[],
    'error':'',
    'successMessage':''
    }

def checkSubCommandConf():
    global result
    if not (os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json")):
        shutil.copyfile(os.path.dirname(os.path.realpath(__file__))+"/subCommandConfSample.json",os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json")
        result['code']=1
        result['content']=[]
        logger.loggerError("This command requires some parameters to be filled in subCommandConf.json. Operation Concluded.")
        result['error']='This command requires some parameters to be filled in subCommandConf.json'
        result['successMessage']=''
        return False
    else:
        return True

def vectorFeatureIdentifier():
    responseSet =  modifierExecutor()
    vecAnalzyer(responseSet['extractor'],responseSet['folderPath'],dbManager.read('loopSections'))
    vecMlModelExecutor(responseSet['folderPath'],responseSet['extractor'])


def schedulingIdentifier():
    responseSet =  modifierExecutor()
    schdedulerInitializer(responseSet['extractor'],responseSet['folderPath'])


def reportGen():
    reportObj = {}
    reportObj['totalExeTime'] = 100
    reportObj['gpuOptTime'] = 20
    reportObj['cpuOptTime'] = 45
    reportObj['vecOptTime'] = 10
    reportObj['notOptTime'] = 10
    reportObj['gpuExeTime'] = 15
    reportObj['cpuExeTime'] = 40
    reportObj['vecExeTime'] = 45
    reportObj['loopLines'] = ['10:18','20:26']
    reportObj['notOptLoopTimes'] = [10,8]
    reportObj['optLoopTimes'] = [8,6]
    reportGenerator(reportObj)


def vectorizer():
    if (checkSubCommandConf()):
        from Extractor.Extractor import Extractor
        commadName = commandJson['command']['vectorize']
        folderPath = commadName['folderPath']
        sourceDirectry = folderPath
        logger.loggerInfo("Extractor Initiated")
        extractor = Extractor(sourceDirectry)
        logger.loggerInfo("Extractor Completed")
        # logger.loggerInfo("System Information Fetcher Initiated")
        # responseObj = __systemInformationIdentifier()
        # if (responseObj['returncode'] == 1):
        #     dbManager.write('systemData', responseObj['content'])
        #     logger.loggerSuccess("System Information Fetcher completed successfully")
        # else:
        #     logger.loggerError("System Information Fetcher Failed")
        #     print "System Information Fetcher Failed. Optimization process terminated."
        #     exit()

        # Runtime arg extraction Initiated
        logger.loggerInfo("Run time arguments fetcher Initiated")
        with open(sourceDirectry + '/run.json') as runArgumentFile:
            dataArguments = json.load(runArgumentFile)
        if not (dataArguments['runTimeArguments'] == None):
            dbManager.overWrite('runTimeArguments', str(dataArguments['runTimeArguments']))
        else:
            logger.loggerError("Run time arguments fetcher Failed. Optimization process terminated.")
            print "Run time arguments fetcher Failed. Optimization process terminated."
            exit()
        logger.loggerSuccess("Run time arguments fetcher completed successfully")
        # Runtime arg extraction Completed

        # Primary Execution Initiated
        from Evaluator.initializer import initExecutor
        logger.loggerInfo("Primary Execution Initiated")
        responseObj = initExecutor(sourceDirectry, dbManager.read('runTimeArguments'))
        if responseObj['returncode'] == 1:
            logger.loggerSuccess("Primary Execution completed successfully.")
            print "initial execution time - " + str(dbManager.read('iniExeTime'))
        else:
            logger.loggerError(responseObj['error'])
            logger.loggerError("Primary Execution Failed. Optimization process terminated.")
            exit()
        # Primary Execution Completed
        # Identifier Initiated
        from Identifier.initializer import identify
        logger.loggerInfo("Source Code Identification Process Initiated")
        response = identify(extractor, sourceDirectry)
        if response['returncode'] == 0:
            logger.loggerSuccess("Source Code Identification Process Completed Successfully")

        else:
            logger.loggerError("Source Code Identification Process Failed. Optimization process terminated.")
            return False
        # Identifier Completed
        vectorizer = Vectorizer(extractor, folderPath)
        vectorizer.initOptimizations()

        # for file in extractor.getSourcePathList():
        #     outerLoops = dbManager.read('loopSections')
        #     for loop in outerLoops:
        #         vectorizer.optimizeAffinity(file, [int(loop["startLine"]), int(loop["endLine"])])



        # vectorizer.vectorize(23)

def modifierExecutor():

    global result
    if(checkSubCommandConf()):
        from Extractor.Extractor import Extractor
        commadName = commandJson['command']['modifierExecute']
        folderPath = commadName['folderPath']
        filePathOld = commadName['filePath']
        logger.loggerInfo("Modifier Execution Command Initiated")
        sourceDirectry = folderPath
        extractor = Extractor(sourceDirectry)
        logger.loggerInfo("System Information Fetcher Initiated")
        responseObj = __systemInformationIdentifier()

        if(responseObj['returncode']==1):
            dbManager.write('systemData',responseObj['content'])
            logger.loggerSuccess("System Information Fetcher completed successfully")
        else:
            logger.loggerError("System Information Fetcher Failed")
            print "System Information Fetcher Failed. Optimization process terminated."
            exit()
        logger.loggerInfo("Run time arguments fetcher Initiated")
        with open(folderPath+'/run.json') as runArgumentFile:
            dataArguments = json.load(runArgumentFile)
        if not (dataArguments['runTimeArguments'] == None):
            dbManager.write('runTimeArguments',str(dataArguments['runTimeArguments']))
        else:
            logger.loggerError("Run time arguments fetcher Failed. Optimization process terminated.")
            print "Run time arguments fetcher Failed. Optimization process terminated."
            exit()

        logger.loggerSuccess("Run time arguments fetcher completed successfully")
        logger.loggerInfo("Profile Summarization Initiated")
        summarizedReport = getSummary(folderPath,dbManager.read('runTimeArguments'))
        if summarizedReport['returncode'] == 1:
            logger.loggerSuccess("Profile Summarization completed successfully")
            optimizableLoops = summarizedReport['content']
            selectedLoops = []
            summaryLoops = []
            for loopSection in optimizableLoops:
                selectedSection = {
                    'fileName': optimizableLoops[loopSection]['fileName'],
                    'identifier': loopSection,
                    'startLine': optimizableLoops[loopSection]['startLine'],
                    'endLine': optimizableLoops[loopSection]['endLine'],
                    'serialStartLine':0,
                    'serialEndLine':0,
                    'executionTime': optimizableLoops[loopSection]['sectionTime'],
                    'optimiazability': False,
                    'optimizeMethod': None
                }
                summarySection = {
                'fileName':optimizableLoops[loopSection]['fileName'],
                'startLine': optimizableLoops[loopSection]['startLine'],
                'endLine':optimizableLoops[loopSection]['endLine'],
                'executionTime':optimizableLoops[loopSection]['sectionTime'],
                'optimiazability':False,
                'optimizedTime':0,
                'optimizeMethod': None
                }
                if (float(optimizableLoops[loopSection]['overheadPrecentage']) > 0.0):
                    selectedSection['optimiazability'] = True
                    summarySection['optimiazability'] = True
                selectedLoops.append(selectedSection)
                summaryLoops.append(summarySection)
            dbManager.write('loopSections', selectedLoops)
            dbManager.write('summaryLoops', summaryLoops)
            workingDir = folderPath + "/_profiling/Sandbox"
            if os.path.exists(workingDir):
                shutil.rmtree(workingDir)
            os.makedirs(workingDir)
            for fileModify in os.listdir(folderPath):
                filePath = folderPath + "/" + fileModify
                if os.path.isfile(filePath):
                    if fileModify.endswith(".c"):
                        sourceObj = extractor.getSource(filePath)
                        sourceObj.writeToFile(workingDir + "/" + fileModify, sourceObj.root)
                        sourceObj.writeToFile(workingDir + "/" + fileModify[:-2] + "_serial.c", sourceObj.serialroot)
                    else:
                        shutil.copyfile(filePath, workingDir + "/" + fileModify)
            with open(folderPath + "/_profiling/Sandbox/Makefile", 'r') as file:
                filedata = file.read()
                filedata = filedata.replace('.c', '_serial.c')
            with open(folderPath + "/_profiling/Sandbox/Makefile", 'w') as file:
                file.write(filedata)
            serialSections = []
            parallelSections = []
            sourceObj = extractor.getSource(filePathOld)
            for item in sourceObj.serialParallelOuterLoopMap():
                for subItem in sourceObj.serialParallelOuterLoopMap()[item]:
                    if item == "serial":
                        serialSections.append(str(subItem.lineNumber) + ":" + str(subItem.endLineNumber))
                    else:
                        parallelSections.append(str(subItem.lineNumber) + ":" + str(subItem.endLineNumber))

            for index, element in enumerate(serialSections):
                parallelStartLine = parallelSections[index].split(":")[0]
                parallelEndLine = parallelSections[index].split(":")[1]
                for data in selectedLoops:
                    # Can have the file Name restrictions if required.
                    if (data['startLine'] == str(int(parallelStartLine) - 1)):

                        if (data['endLine'] == parallelEndLine):
                            if (data['optimiazability']):
                                data['serialStartLine'] = str(int(element.split(":")[0]) - 1)
                                data['serialEndLine']= str(int(element.split(":")[1]) + 1)
                                break
            dbManager.overWrite('loopSections', selectedLoops)
        return {'extractor':extractor,'folderPath':folderPath}


def mlGPUDataMode():
    if(checkSubCommandConf()):
        commadName = commandJson['command']['mlGUPModel']
        resultLocal = mlModelExecutor(commadName['filePath'])
        if (resultLocal):
            result['code']=0
            result['content']=resultLocal
            result['error']=''
            result['successMessage']='GPU machine learning process concluded successfully'
            logger.loggerSuccess("GPU machine learning process concluded successfully")
        else:
            result['code']=1
            result['content']=[]
            result['error']='GPU machine learning model failed'
            result['successMessage']=''
            logger.loggerError("GPU machine learning model Failed")



def nonArchi():
    global result
    logger.loggerInfo("nonArchiFeatureFetch command Initiated")
    if(checkSubCommandConf()):
        commadName = commandJson['command']['nonArchiFeatureFetch']
        resultLocal = hotspotsProfiler(commadName['codeName'],commadName['mainFile'],commadName['annotatedFile'],commadName['makeFile'],commadName['compilerOprtions'],commadName['arguments'],commadName['loopSegments'],os.path.dirname(os.path.realpath(__file__)))
        if (resultLocal):
            result['code']=0
            result['content']=resultLocal
            result['error']=''
            result['successMessage']='Feature extraction concluded successfully'
            logger.loggerSuccess("Feature extraction concluded and nonArchiFeatureFetch command concluded successfully")
        else:
            result['code']=1
            result['content']=[]
            result['error']='Feature extraction failed'
            result['successMessage']=''
            logger.loggerError("Feature extraction failed and nonArchiFeatureFetch command concluded")

def occupancyCal():
    global result
    logger.loggerInfo("occupancyCal Command Initiated")
    if(checkSubCommandConf()):
        commadName = commandJson['command']['occupencyCalculate']
        resultLocal = occupancyCalculation(commadName['computeCapability'],commadName['registersPerThread'],commadName['sharedMemoryPerBlock'])
        result['code']=0
        result['content']=resultLocal
        result['error']=''
        result['successMessage']=''
        logger.loggerSuccess("occupancyCal command concluded successfully")

def offloadOptimizer():
        global result
        logger.loggerInfo("offloadOptimizer Command Initiated")
        if(checkSubCommandConf()):
            modifireReturn = modifierExecutor()
            #commadName = commandJson['command']['offloadOptimizer']
            resultLocal = runOffloadOptimizer(modifireReturn['extractor'], modifireReturn['folderPath'])
            result['code']=0
            result['content']=resultLocal
            result['error']=''
            result['successMessage']=''
            logger.loggerSuccess("offloadOptimizer command concluded successfully")


def systemIdentify():
    global result
    logger.loggerInfo("System Data Identifier Command Initiated")
    if(__systemInformationIdentifier()['returncode']==1):
        with open(os.path.dirname(os.path.realpath(__file__))+"/Identifier/systemIdentifier/sysinfo/systemInfo.json", 'r') as handle:
            parsed = json.load(handle)
        # print json.dumps(parsed, indent=4, sort_keys=True)
        result['code']=0
        result['content']=parsed
        result['error']=''
        result['successMessage']='System data identification Completed'
        logger.loggerSuccess("System data identification Completed and System Data Identifier command concluded successfully")
    else:
        result['code']=1
        result['content']=[]
        result['error']='System data identification Failed'
        result['successMessage']=''
        logger.loggerError("System data identification failed and System Data Identifier command concluded")

    if(os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/deviceQuery") ):
        os.remove(os.path.dirname(os.path.realpath(__file__))+"/deviceQuery")

def sourceAnnotation():
    global result
    logger.loggerInfo("Source Code Annotation Command Initiated")
    if(checkSubCommandConf()):
        commadName = commandJson['command']['sourceCodeAnnotation']
        if (os.path.isfile(commadName['annotatedFile'])):
            subFilePath = commadName['annotatedFile'].split("Sandbox")[1]
            if(os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/Identifier/identifierSandbox/sourceCodeAnnotation/Sandbox")):
                shutil.rmtree(os.path.dirname(os.path.realpath(__file__))+"/Identifier/identifierSandbox/sourceCodeAnnotation/Sandbox")
            shutil.copytree("./Sandbox", os.path.dirname(os.path.realpath(__file__))+"/Identifier/identifierSandbox/sourceCodeAnnotation/Sandbox")
            resultLocal = targetDataMap(subFilePath,commadName['annotationStartLine'],commadName['annotationEndLine'],commadName['annotatedFile'])
            if (resultLocal["code"]):
                result['code']=0
                result['content']=resultLocal['data']
                result['error']=''
                result['successMessage']='Source Code Annotation concluded successfully'

            else:
                result['code']=1
                result['content']=[]
                result['error']="Source Code Annotation failed" + resultLocal["message"]
                result['successMessage']=''
        else:
            result['code']=1
            result['content']=[]
            result['error']="unable to find file : " + commadName['annotatedFile']
            result['successMessage']=''


def arrayInformationFetch():
    global result
    logger.loggerInfo("Array Information Fetch Command Initiated")
    if(checkSubCommandConf()):
        commadName = commandJson['command']['arrayInfoFetch']
        if (os.path.isfile(commadName['annotatedFile'])):
            subFilePath = commadName['annotatedFile'].split("Sandbox")[1]
            if(os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/Identifier/identifierSandbox/arrayInfoIdentifier/Sandbox")):
                shutil.rmtree(os.path.dirname(os.path.realpath(__file__))+"/Identifier/identifierSandbox/arrayInfoIdentifier/Sandbox")
            shutil.copytree("./Sandbox", os.path.dirname(os.path.realpath(__file__))+"/Identifier/identifierSandbox/arrayInfoIdentifier/Sandbox")
            resultLocal = arrayInfoFetch(subFilePath,commadName['infoFetchStartLine'],commadName['infoFetchEndLine'])
            if (resultLocal["code"]):
                result['code']=0
                result['content']=resultLocal['data']
                result['error']=''
                result['successMessage']='Information Fetch Concluded Successfully'
            else:
                result['code']=1
                result['content']=[]
                result['error']="Information Fetch failed"
                result['successMessage']=''
        else:
            result['code']=1
            result['content']=[]
            result['error']="unable to find file : " + commadName['annotatedFile']
            result['successMessage']=''

def runCommand(command):
    commandSegments = {
        'nonArchiFeatureFetch': lambda : nonArchi(),
        'occupencyCalculate': lambda : occupancyCal(),
        'systemIdentify':lambda : systemIdentify(),
        'sourceAnnotation': lambda : sourceAnnotation(),
        'arrayInfoFetch':lambda : arrayInformationFetch(),
        'mlGUPModel':lambda : mlGPUDataMode(),
        'offloadOptimizer':lambda :offloadOptimizer(),
        'modifierExecute':lambda :modifierExecutor(),
        "vectorize":lambda :vectorizer(),
        'schedule':lambda :schedulingIdentifier(),
        'vectorFeature': lambda: vectorFeatureIdentifier(),
        'report': lambda: reportGen()

    }[command]()

    return result

if __name__ == "__main__":
    logger.createLog()
    logger.loggerInfo("Individual Command executer initiated")
    if os.path.isfile('/media/pasindu/newvolume/FYP/Framework/Rigel-FYP/DatabaseManager/rigel.db'):
        os.remove('/media/pasindu/newvolume/FYP/Framework/Rigel-FYP/DatabaseManager/rigel.db')
    if(len(sys.argv)>1):
        runCommand(sys.argv[1])
        if(result['code']==0):
            if not result['successMessage'] == "":
                print result['successMessage']
            if not result['content'] == []:
                print result['content']
            logger.loggerSuccess("Individual Command executer completed successfully")
        if(result['code']==1):
            if not result['error'] == "":
                print result['error']
                logger.loggerError("Individual Command executer completed with error : "+str(result['error']))
            else :
                print "Unknown Error"
                logger.loggerError("Individual Command executer completed with unknown Error")
    else:
        print "Please add the command name"
        logger.loggerError("Command Name missing")
