import os
import sys
import argparse
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Utils")
from Identifier.ini  import trigger


parser = argparse.ArgumentParser(description='Initilizer of optimizer')
parser.add_argument('-fp', '--fpath', type=str, help='Absolute file path', required=True)
parser.add_argument('-fa', '--farguments', type=str, help='Runtime file arguments', required=False, default="")
args = parser.parse_args()
response = {
    "returncode":0,
    "error":"",
    "content":{}
    }
arguments = {
    "fileAbsPath":args.fpath,
    "fileArguments":args.farguments
    }

try:
    responseObj = trigger(arguments['fileAbsPath'],arguments['fileArguments'])
    if (responseObj['returncode'] == 1):
        response['error'] = ""
        response['content'] = responseObj['content']
        response['returncode'] = 1
        print "Optimization Concluded Successfully "
except Exception as e:
    print e
    print "Unexpected Error Occured."
    response['error'] = e
    response['content'] = {}
    response['returncode'] = 0
