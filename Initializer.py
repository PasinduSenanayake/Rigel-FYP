import os
import sys
import argparse
from Extractor.Extractor import Extractor
from Vectorizer.Vectorizer import Vectorizer
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Utils")
from Identifier.ini  import trigger
from shutil import copyfile
import shutil

parser = argparse.ArgumentParser(description='Initializer of optimizer')
parser.add_argument('-fd', '--fdirectory', type=str, help='Absolute file directory', required=True)
# parser.add_argument('-fp', '--fpath', type=str, help='Absolute file path', required=True)
# parser.add_argument('-ca', '--carguments', type=str, help='Compiler time arguments', required=False, default="")
# parser.add_argument('-fa', '--farguments', type=str, help='Run time arguments', required=False, default="")
args = parser.parse_args()
# response = {
#     "returncode":0,
#     "error":"",
#     "content":{}
#     }
# arguments = {
#     "fileAbsPath":args.fpath,
#     "runTimeArguments":args.farguments,
#     "compTimeArguments":args.carguments
#     }

# try:
#     responseObj = trigger(arguments['fileAbsPath'],arguments['compTimeArguments'],arguments['runTimeArguments'])
#     if (responseObj['returncode'] == 1):
#         response['error'] = ""
#         response['content'] = responseObj['content']
#         response['returncode'] = 1
#         print "Optimization Concluded Successfully "
#     else:
#         print responseObj
# except Exception as e:
#     print e
#     print "Unexpected Error Occured."
#     response['error'] = e
#     response['content'] = {}
#     response['returncode'] = 0

### EXTRACTOR ###


extractor = Extractor(args.fdirectory)

##profiling init
directoryName = args.fdirectory.split("/")[-1]
workingDir = args.fdirectory + "/_profiling"
if os.path.exists(workingDir):
    shutil.rmtree(workingDir)
os.makedirs(workingDir)

for file in os.listdir(args.fdirectory):
    filePath = args.fdirectory + "/" + file
    if os.path.isfile(filePath):
        if file.endswith(".c"):
            sourceObj = extractor.getSource(filePath)
            sourceObj.writeToFile(workingDir + "/" + file, sourceObj.root)
            sourceObj.writeToFile(workingDir + "/" + file[:-2] + "_serial.c", sourceObj.serialroot)
        else:
            copyfile(filePath, workingDir + "/" + file)

### VECTORIZING ###

vectorizer = Vectorizer(extractor, args.fdirectory)




