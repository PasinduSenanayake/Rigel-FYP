import json,os,sys
from Identifier.nonarchiFeatureFetcher import hotspotsProfiler

with open(os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json") as f:
    commandJson = json.load(f)

def nonArchi():
    commadName = commandJson['command']['nonArchiFeatureFetch']
    result = hotspotsProfiler(commadName['codeName'],commadName['mainFile'],commadName['subFiles'],commadName['compilerOprtions'],commadName['arguments'],commadName['loopSegments'],os.path.dirname(os.path.realpath(__file__)))
    if (result):
        print "Feature extraction concluded successfully"
    else:
        print "Feature extraction failed"
def runCommand(command):
    commandSegments = {
        'nonArchiFeatureFetch': lambda : nonArchi()
    }[command]()


runCommand(sys.argv[1])
