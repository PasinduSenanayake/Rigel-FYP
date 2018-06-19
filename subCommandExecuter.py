import json,os,sys
from Identifier.nonarchiFeatureFetcher import hotspotsProfiler

with open(os.path.dirname(os.path.realpath(__file__))+"/subCommandConf.json") as f:
    commandJson = json.load(f)

def nonArchi():
    commadName = commandJson['command']['nonArchiFeatureFetch']
    hotspotsProfiler(commadName['mainFile'],commadName['subFiles'],commadName['compilerOprtions'],commadName['arguments'],commadName['loopSegments'])

def runCommand(command):
    commandSegments = {
        'nonArchiFeatureFetch': lambda : nonArchi()
    }[command]()


runCommand(sys.argv[1])
