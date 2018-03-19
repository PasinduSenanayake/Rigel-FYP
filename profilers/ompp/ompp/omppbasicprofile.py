import subprocess
import os
import shutil
import platform


def getBasicProfile(filePath, arguments=""):
    shutil.copy2(filePath, os.getcwd()+'/test.c')
    omppPath =  str(os.path.dirname(os.path.realpath(__file__)))+"/ompp/bin/kinst-ompp"
    omppPath2 = str(os.path.dirname(os.path.realpath(__file__)))+"/ompp/lib"
    stderr = None
    outPut = {
    "error":"",
    "content":""
    }
    if(platform.system() == "Linux"):
        temp_env = os.environ.copy()
        temp_env['OMPP_OUTFORMAT']='csv'
        processOutput = subprocess.Popen(omppPath+' gcc -L'+omppPath2+' -lompp -fopenmp test.c -o testapp',env=temp_env,shell=True, stderr=subprocess.PIPE)
        stdout, stderr = processOutput.communicate()
        if(stderr == ""):
            processOutput = subprocess.Popen('./testapp '+str(arguments),env=temp_env,shell=True, stderr=subprocess.PIPE)
            stdout, stderr = processOutput.communicate()
            if(stderr == ""):
                with open('unknown.4-0.ompp.csv') as fileData:
                    outPut['content'] = fileData.readlines()
    else:
        stderr ="unknown platform"
        
    if(stderr == ""):
        os.remove('test.c')
        os.remove('test.c.opari.inc')
        os.remove('test.mod.c')
        os.remove('opari.rc')
        os.remove('opari.tab.c')
        os.remove('opari.tab.o')
        os.remove('testapp')
        os.remove('unknown.4-0.ompp.csv')
    else:
        outPut['error']= stderr
    return outPut
