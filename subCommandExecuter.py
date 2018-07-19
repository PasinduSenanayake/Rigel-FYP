import json,os,sys
import shutil

from Identifier.nonarchiFeatureFetcher import hotspotsProfiler
from Identifier.offloadChecker import occupancyCalculation
from Identifier.systemIdentifier import __systemInformationIdentifier
from Identifier.identifierSandbox.sourceCodeAnnotation.sourceAnnotator import targetDataMap
from Identifier.identifierSandbox.arrayInfoIdentifier.arrayInfoFetcher import arrayInfoFetch

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
        result['error']='This command requires some parameters to be filled in subCommandConf.json'
        result['successMessage']=''
        return False
    else:
        return True

def nonArchi():
    global result
    if(checkSubCommandConf()):
        commadName = commandJson['command']['nonArchiFeatureFetch']
        resultLocal = hotspotsProfiler(commadName['codeName'],commadName['mainFile'],commadName['annotatedFile'],commadName['makeFile'],commadName['compilerOprtions'],commadName['arguments'],commadName['loopSegments'],os.path.dirname(os.path.realpath(__file__)))
        if (resultLocal):
            result['code']=0
            result['content']=resultLocal
            result['error']=''
            result['successMessage']='Feature extraction concluded successfully'
        else:
            result['code']=1
            result['content']=[]
            result['error']='Feature extraction failed'
            result['successMessage']=''

def occupancyCal():
    global result
    if(checkSubCommandConf()):
        commadName = commandJson['command']['occupencyCalculate']
        resultLocal = occupancyCalculation(commadName['computeCapability'],commadName['registersPerThread'],commadName['sharedMemoryPerBlock'])
        result['code']=0
        result['content']=resultLocal
        result['error']=''
        result['successMessage']=''

def systemIdentify():
    global result
    if(__systemInformationIdentifier()['returncode']==1):
        with open(os.path.dirname(os.path.realpath(__file__))+"/Identifier/sysinfo/systemInfo.json", 'r') as handle:
            parsed = json.load(handle)
        # print json.dumps(parsed, indent=4, sort_keys=True)
        result['code']=0
        result['content']=parsed
        result['error']=''
        result['successMessage']='System data indentification Completed'
    else:
        result['code']=1
        result['content']=[]
        result['error']='System data indentification Failed'
        result['successMessage']=''

    if(os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/deviceQuery") ):
        os.remove(os.path.dirname(os.path.realpath(__file__))+"/deviceQuery")

def sourceAnnotation():
    global result
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
    }[command]()

    return result

# if len(sys.argv) > 1:
#     runCommand(sys.argv[1])
#     if(result['code']==0):
#         if not result['successMessage'] == "":
#             print result['successMessage']
#         if not result['content'] == []:
#             print result['content']
#     if(result['code']==1):
#         if not result['error'] == "":
#             print result['error']
#         else :
#             print "Unknow error occured. Process failed."
