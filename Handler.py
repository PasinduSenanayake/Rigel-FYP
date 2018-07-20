import sys
import platform
import json
import subprocess
import os
import shutil,logger
from DependencyManager.InternalManager import *

depPath = str(os.path.dirname(os.path.realpath(__file__)))+"/Utils"
print "Making SystemDependencies persistance."
src = str(os.path.dirname(os.path.realpath(__file__)))+"/Utils"
dst = str(os.path.dirname(os.path.realpath(__file__)))+"/UtilsTemp"
shutil.copytree(src, dst)

def issuccessUp():
    status = {
        "error":"",
        "code":0
        }
    response = updateLocal()
    if(response['code']==1):
        response = updateRequirementFile()
        if(response['code']==1):
            status['code'] = 1
        else :
            status['code'] = 0
            status['error'] = response['error']
    else:
        status['code'] = 0
        status['error'] = response['error']
    return status

def installDep(module,version):
    try:
        response = moduleCheck(module, version)
        if not (response['code'] == 0):
            if(response['code']==1):
                print response['info']
                print "Please uninstall before install the module."
            elif(response['code']==2):
                print response['info']
                processOutput = subprocess.Popen('pip --disable-pip-version-check install --target='+depPath+' '+module+'=='+version+' --upgrade',shell=True, stderr=subprocess.PIPE)
                stdout, stderr = processOutput.communicate()
                if(stderr== ""):
                    updateState = updateMain("update",module,version)
                    if(updateState['code']==1):
                        responseStatus = issuccessUp()
                        if(responseStatus['code']==1):
                            print "Module upgraded successfully."
                            shutil.rmtree(dst)
                        else :
                            shutil.rmtree(src)
                            shutil.copytree(dst, src)
                            shutil.rmtree(dst)
                            reverseback()
                            print responseStatus['error']
                            print "Module upgrade failed. Rolledback to previous state."
                    else :
                        shutil.rmtree(src)
                        shutil.copytree(dst, src)
                        shutil.rmtree(dst)
                        reverseback()
                        print updateState['error']
                        print "Module upgrade failed. Rolledback to previous state."
                else:
                    shutil.rmtree(src)
                    shutil.copytree(dst, src)
                    shutil.rmtree(dst)
                    reverseback()
                    print stderr
                    print "Module upgrade failed. Rolledback to previous state."
            elif(response['code']==3):
                print response['info']
                processOutput = subprocess.Popen('pip --disable-pip-version-check install --target='+depPath+' '+module+'=='+version+'',shell=True, stderr=subprocess.PIPE)
                stdout, stderr = processOutput.communicate()
                if(stderr== ""):
                    updateState = updateMain("install",module,version)
                    if(updateState['code']==1):
                        responseStatus = issuccessUp()
                        if(responseStatus['code']==1):
                            print "Module installed successfully."
                            shutil.rmtree(dst)
                        else :
                            shutil.rmtree(src)
                            shutil.copytree(dst, src)
                            shutil.rmtree(dst)
                            reverseback()
                            print responseStatus['error']
                            print "Module installation failed. Rolledback to previous state."
                    else:
                        shutil.rmtree(src)
                        shutil.copytree(dst, src)
                        shutil.rmtree(dst)
                        reverseback()
                        print updateState['error']
                        print "Module installation failed. Rolledback to previous state."
                else:
                    shutil.rmtree(src)
                    shutil.copytree(dst, src)
                    shutil.rmtree(dst)
                    reverseback()
                    print stderr
                    print "Module installation failed. Rolledback to previous state."
        else:
            shutil.rmtree(dst)
            print response['error']
    except Exception as e:
        print e
        shutil.rmtree(src)
        shutil.copytree(dst, src)
        shutil.rmtree(dst)
    removeTemp()

def uninstallDep(module,version):
    try:
        response = moduleCheck(module, version)
        if (response['code'] == 1):
            updateStatus = updateMain("uninstall",module)
            if(updateStatus['code']==1):
                responseStatus = issuccessUp()
                if(responseStatus['code']==1):
                    while(True):
                        responseString = raw_input("Dependencies adjusted. Do you want to remove all the files related to that module. This may take long time as well as internet data. (Y/n): ")
                        if(responseString=="Y"):
                            stderr =""
                            shutil.rmtree(src)
                            if not (os.stat("DependencyManager/requirements.txt").st_size == 0):
                                processOutput = subprocess.Popen('pip --disable-pip-version-check install --target='+depPath+' -r DependencyManager/requirements.txt',shell=True,stderr=subprocess.PIPE)
                                stdout, stderr = processOutput.communicate()
                            else:
                                 os.makedirs(src)
                            if(stderr == ""):
                                print "Module uninstalled successfully."
                                shutil.rmtree(dst)
                            else:
                                print stderr
                                shutil.copytree(dst, src)
                                shutil.rmtree(dst)
                                reverseback()
                                print "Module uninstallation failed. Rolledback to previous state."
                            break
                        elif(responseString=="n"):
                            print "Module uninstalled successfully."
                            shutil.rmtree(dst)
                            break
                        else:
                            print "Please provide Y or n \n"
                else :
                    shutil.rmtree(src)
                    shutil.copytree(dst, src)
                    shutil.rmtree(dst)
                    reverseback()
                    print updateStatus['error']
                    print "Module uninstallation failed. Rolledback to previous state."
            else:
                shutil.rmtree(src)
                shutil.copytree(dst, src)
                shutil.rmtree(dst)
                reverseback()
                print responseStatus['error']
                print "Module uninstallation failed. Rolledback to previous state."

        elif response['code'] == 2:
            shutil.rmtree(dst)
            print "Different version of the module has been installed. Process terminated"
        elif response['code'] == 3:
            shutil.rmtree(dst)
            print "No such module has been installed"
        else:
            shutil.rmtree(dst)
            print response['error']
    except Exception as e:
        print e
        shutil.rmtree(src)
        shutil.copytree(dst, src)
        shutil.rmtree(dst)
    removeTemp()

def updateAll():
    refreshedData = updateCheck()
    print "Initiate upgrading"
    process = True
    for key in refreshedData['info']['upgrade'].keys():
        process = updateDep(key, refreshedData['info']['upgrade'][key])
        if not (process):
            reverseback()
    if process:
        for key in refreshedData['info']['install'].keys():
            process = updateDep(key, refreshedData['info']['install'][key])
            if not (process):
                reverseback()
    if process:
        responseStatus = issuccessUp()
        if(responseStatus['code']==1):
            print "Upgrade Concluded successfully"
            print str(len(refreshedData['info']['upgrade'].keys()))+"packages were upgraded"
            print str(len(refreshedData['info']['install'].keys()))+"packages were installed"
            shutil.rmtree(dst)
        else :
            shutil.rmtree(src)
            shutil.copytree(dst, src)
            shutil.rmtree(dst)
            reverseback()
            print responseStatus['error']
            print "Module upgrade failed. Rolledback to previous state."
    else:
        shutil.rmtree(src)
        shutil.copytree(dst, src)
        shutil.rmtree(dst)
        reverseback()
        print "Upgrade failed. Rolledback"
    removeTemp()



def updateDep(module,version):
    isSuccess = True
    try:
        response = moduleUpdateCheck(module, version)
        if not (response['code'] == 0):
            if(response['code']==2):
                print response['info']
                processOutput = subprocess.Popen('pip --disable-pip-version-check install --target='+depPath+' '+module+'=='+version+' --upgrade',shell=True, stderr=subprocess.PIPE)
                stdout, stderr = processOutput.communicate()
                if(stderr== ""):
                    print module+" Module upgraded successfully."
                else:
                    isSuccess = False
                    print stderr
                    print module+" Module upgrade failed"
            elif(response['code']==3):
                print response['info']
                processOutput = subprocess.Popen('pip --disable-pip-version-check install --target='+depPath+' '+module+'=='+version+'',shell=True, stderr=subprocess.PIPE)
                stdout, stderr = processOutput.communicate()
                if(stderr== ""):
                    print module+" Module installed successfully."
                else:
                    isSuccess = False
                    print stderr
                    print module+" Module installation failed."
        else:
            print response['error']
            isSuccess = False
    except Exception as e:
        print e
        isSuccess = False
    return isSuccess

def updateAllInit():
    finalState = True
    refreshedData = updateCheck()
    process = True
    for key in refreshedData['info']['upgrade'].keys():
        process = updateDepInit(key, refreshedData['info']['upgrade'][key])
        if not (process):
            reverseback()
    if process:
        for key in refreshedData['info']['install'].keys():
            process = updateDepInit(key, refreshedData['info']['install'][key])
            if not (process):
                reverseback()
    if process:
        responseStatus = issuccessUp()
        if(responseStatus['code']==1):
            shutil.rmtree(dst)
        else :
            shutil.rmtree(src)
            shutil.copytree(dst, src)
            shutil.rmtree(dst)
            finalState = False
            reverseback()

    else:
        shutil.rmtree(src)
        shutil.copytree(dst, src)
        shutil.rmtree(dst)
        finalState = False
        reverseback()
    removeTemp()
    return finalState


def updateDepInit(module,version):
    isSuccess = True
    try:
        response = moduleUpdateCheck(module, version)
        if not (response['code'] == 0):
            if(response['code']==2):
                processOutput = subprocess.Popen('pip --disable-pip-version-check install --target='+depPath+' '+module+'=='+version+' --upgrade',shell=True, stderr=subprocess.PIPE)
                stdout, stderr = processOutput.communicate()
                if not (stderr== ""):
                    logger.loggerError("Update Faile with error : "+stderr)
                    isSuccess = False
            elif(response['code']==3):
                processOutput = subprocess.Popen('pip --disable-pip-version-check install --target='+depPath+' '+module+'=='+version+'',shell=True, stderr=subprocess.PIPE)
                stdout, stderr = processOutput.communicate()
                if not (stderr== ""):
                    logger.loggerError("Update Faile with error : "+stderr)
                    isSuccess = False
        else:
            isSuccess = False
    except Exception as e:
        logger.loggerError("Update Faile with error : "+str(e))
        isSuccess = False
    return isSuccess

if __name__ == "__main__":
    if len(sys.argv)>1:
        if(sys.argv[1]=="install"):
            if len(sys.argv) == 4:
                if not (sys.argv[2].isspace() or sys.argv[3].isspace()):
                    installDep(sys.argv[2],sys.argv[3])
                else:
                    print "Install requires [Module Name] [Version]. Please enter arguments correctly"
                    shutil.rmtree(dst)
                    removeTemp()
            else:
                print "Install requires [Module Name] [Version]. Please enter arguments correctly"
                shutil.rmtree(dst)
                removeTemp()
        elif(sys.argv[1]=="uninstall"):
            if len(sys.argv) == 4:
                if not (sys.argv[2].isspace() or sys.argv[3].isspace()):
                    uninstallDep(sys.argv[2],sys.argv[3])
                else:
                    print "Uninstall requires [Module Name] [Version]. Please enter arguments correctly"
                    shutil.rmtree(dst)
                    removeTemp()
            else:
                print "Uninstall requires [Module Name] [Version]. Please enter arguments correctly"
                shutil.rmtree(dst)
                removeTemp()

        elif(sys.argv[1]=="updateAll"):
            updateAll()
        else:
            print "Please enter arguments correctly"
            shutil.rmtree(dst)
            removeTemp()
    else:
        print "Required parameters are missing. Please follow the API documentation in github."
        shutil.rmtree(dst)
        removeTemp()
