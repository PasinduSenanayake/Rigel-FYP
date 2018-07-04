import json,os,sys
import shutil

from Identifier.nonarchiFeatureFetcher import hotspotsProfiler
from Identifier.offloadChecker import occupancyCalculation
from Identifier.systemIdentifier import __systemInformationIdentifier
from Identifier.identifierSandbox.sourceCodeAnnotation.sourceAnnotator import targetDataMap

if(os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json")):
    with open(os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json") as f:
        commandJson = json.load(f)

def checkSubCommandConf():
    if not (os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json")):
        shutil.copyfile(os.path.dirname(os.path.realpath(__file__))+"/subCommandConfSample.json",os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json")
        print "This command requires some parameters to be filled in subCommandConf.json"
        return False
    else:
        return True

def nonArchi():
    if(checkSubCommandConf()):
        commadName = commandJson['command']['nonArchiFeatureFetch']
        result = hotspotsProfiler(commadName['codeName'],commadName['mainFile'],commadName['annotatedFile'],commadName['makeFile'],commadName['compilerOprtions'],commadName['arguments'],commadName['loopSegments'],os.path.dirname(os.path.realpath(__file__)))
        if (result):
            print "Feature extraction concluded successfully"
        else:
            print "Feature extraction failed"

def occupancyCal():
    if(checkSubCommandConf()):
        commadName = commandJson['command']['occupencyCalculate']
        result = occupancyCalculation(commadName['computeCapability'],commadName['registersPerThread'],commadName['sharedMemoryPerBlock'])
        print result

def systemIdentify():
    if(__systemInformationIdentifier()['returncode']==1):
        print "System data indentification Completed \n"
        with open(os.path.dirname(os.path.realpath(__file__))+"/Identifier/sysinfo/systemInfo.json", 'r') as handle:
            parsed = json.load(handle)
        print json.dumps(parsed, indent=4, sort_keys=True)

    else:
        print "System data indentification Failed"
    if(os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/deviceQuery") ):
        os.remove(os.path.dirname(os.path.realpath(__file__))+"/deviceQuery")

def sourceAnnotation():
    if(checkSubCommandConf()):
        commadName = commandJson['command']['sourceCodeAnnotation']
        if (os.path.isfile(commadName['annotatedFile'])):
            subFilePath = commadName['annotatedFile'].split("Sandbox")[1]
            if(os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/Identifier/identifierSandbox/sourceCodeAnnotation/Sandbox")):
                shutil.rmtree(os.path.dirname(os.path.realpath(__file__))+"/Identifier/identifierSandbox/sourceCodeAnnotation/Sandbox")
            shutil.copytree("./Sandbox", os.path.dirname(os.path.realpath(__file__))+"/Identifier/identifierSandbox/sourceCodeAnnotation/Sandbox")
            result = targetDataMap(subFilePath,commadName['annotationStartLine'],commadName['annotationEndLine'],commadName['annotatedFile'])
            if (result["code"]):
                print "Source Code Annotation concluded successfully"
            else:
                print "Source Code Annotation failed" + result["message"]
        else:
            print "unable to find file : " + commadName['annotatedFile']


def runCommand(command):
    commandSegments = {
        'nonArchiFeatureFetch': lambda : nonArchi(),
        'occupencyCalculate': lambda : occupancyCal(),
        'systemIdentify':lambda : systemIdentify(),
        'sourceAnnotation': lambda : sourceAnnotation()
    }[command]()


runCommand(sys.argv[1])
