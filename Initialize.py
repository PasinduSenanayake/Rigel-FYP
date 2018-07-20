import sys
import subprocess
import os
import shutil

def moduleInit():
    response = {
        'code':0,
        'error':''
        }
    depPath = str(os.path.dirname(os.path.realpath(__file__)))+"/Utils"
    try:
        if(os.path.isdir(depPath)):
            shutil.rmtree(depPath)
        os.makedirs(depPath)
        envReady =False
        processOutputVersion = subprocess.Popen('pip --version',shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutVersion, stderrVersion = processOutputVersion.communicate()
        if(stderrVersion.strip()==""):
            if not str(stdoutVersion).split(' ')[1] == "9.0.1":
                processOutputDowngrade = subprocess.Popen('python -m pip install pip==9.0.1',shell=True)
                stdoutDowngrade, stderrDowngrade = processOutputDowngrade.communicate()
                if(stderrDowngrade==None):
                    envReady = True
                else:
                    response['code'] = 1
                    response['error'] = str(stderrDowngrade)
            else:
                envReady = True
        else:
            response['code'] = 1
            response['error'] = str(stderrVersion)
        if(envReady):
            processOutput = subprocess.Popen('pip --disable-pip-version-check install --target='+depPath+' -r DependencyManager/requirements.txt',shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = processOutput.communicate()
            if(stderr.strip()==""):
                filesPath = str(os.path.dirname(os.path.realpath(__file__)))+"/DependencyManager"
                shutil.copy2(filesPath+'/requirements.json', filesPath+'/requirementsLocal.json')
                print "Modules installed successfully."
            else:
                response['code'] = 1
                response['error'] = stderr
                shutil.rmtree(depPath)
        return response

    except Exception as e:
        response['code'] = 1
        response['error'] = str(e)
        shutil.rmtree(depPath)
        return response

def init():
    depPath = str(os.path.dirname(os.path.realpath(__file__)))+"/Utils"
    try:
        if(os.path.isdir(depPath)):
            shutil.rmtree(depPath)
        os.makedirs(depPath)
        envReady =False
        processOutputVersion = subprocess.Popen('pip --version',shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutVersion, stderrVersion = processOutputVersion.communicate()
        if(stderrVersion.strip()==""):
            if not str(stdoutVersion).split(' ')[1] == "9.0.1":
                processOutputDowngrade = subprocess.Popen('python -m pip install pip==9.0.1',shell=True)
                stdoutDowngrade, stderrDowngrade = processOutputDowngrade.communicate()
                if(stderrDowngrade==None):
                    envReady = True
            else:
                envReady = True
        if(envReady):
            processOutput = subprocess.Popen('pip --disable-pip-version-check install --target='+depPath+' -r DependencyManager/requirements.txt',shell=True)
            stdout, stderr = processOutput.communicate()
            if(stderr==None):
                filesPath = str(os.path.dirname(os.path.realpath(__file__)))+"/DependencyManager"
                shutil.copy2(filesPath+'/requirements.json', filesPath+'/requirementsLocal.json')
                print "Modules installed successfully."
            else:
                print stderr
                shutil.rmtree(depPath)
                print "Modules installation failed."

    except Exception as e:
        print e
        print "Modules installation failed."
        shutil.rmtree(depPath)

if __name__ == "__main__":
    init()
