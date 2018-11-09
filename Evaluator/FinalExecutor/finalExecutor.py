import subprocess
import os
import shutil
import platform
import dbManager
import time

def finalExecution(dirPath,runTimeArguments="", additionalFlags=""):
    response = {
        "error":"",
        "content":{},
        "returncode":0
        }

    if(os.path.isdir(dirPath)):
        if(os.path.isdir(str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")):
            shutil.rmtree(str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")
        shutil.copytree(dirPath, str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")
        lines=[]
        with open(str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox/Makefile") as books:
            lines = books.readlines()
            for index,line in enumerate(lines):
                if '[compiler]' in line:
                    line = line.replace("[compiler]",' clang  -fopenmp -w')
                    lines[index] = line
                if '[targetObject]' in line:
                    line = line.replace("[targetObject]",'testapp')
                    lines[index] = line
                if "flags" in line and "$" not in line and additionalFlags and additionalFlags not in line:
                    line = line[:-1] + " " + additionalFlags + "\n"
                    lines[index] = line
        with open(str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox/Makefile", 'w') as rewriteMake:
            rewriteMake.writelines(lines)
        processOutput = subprocess.Popen('make',shell=True, stderr=subprocess.PIPE,cwd=str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")
        stdout, stderr = processOutput.communicate()
        if(stderr == ""):
            exeStartTime = time.time()
            processOutput = subprocess.Popen(os.path.dirname(os.path.realpath(__file__))+'/sandbox/testapp '+str(runTimeArguments),shell=True, stderr=subprocess.PIPE,cwd=str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")
            stdout, stderr = processOutput.communicate()
            if(stderr == ""):
                exeEndTime = time.time()
                shutil.rmtree(str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")
                dbManager.overWrite('finalExeTime', exeEndTime-exeStartTime)
                response['returncode']=1
            else:
                response['returncode']=0
                response['error']=stderr
                response['content']=stdout
            return response
        else:
            response['returncode']=0
            response['error']=stderr
            response['content']=stdout
        return response
    else:
        response['returncode']=0
        response['error']="Folder Path is incorrect"
        response['content']=stdout
    return response
