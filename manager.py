import sys
import platform
import json
import subprocess
import os
import shutil

depPath = os.getcwd()+"/Utils"
print "Making SystemDependencies persistance."
src = os.getcwd()+"/Utils"
dst = os.getcwd()+"/UtilsTemp"
shutil.copytree(src, dst)

if(sys.argv[1]=="install"):
    fileData = open("requirements.txt","r")
    lines = fileData.readlines()
    fileData.close()
    tempName = None
    fileData = open("requirements.txt","w")
    for line in lines:
        if line.startswith(sys.argv[2]):
            tempName = line
        else:
            fileData.write(line)
    fileData.close()
    if not (tempName):
        processOutput = subprocess.Popen('pip install --target='+depPath+' '+sys.argv[2]+'',shell=True, stderr=subprocess.PIPE)
        stdout, stderr = processOutput.communicate()
        if(stderr== None):
            with open("requirements.txt", "a") as reqFile:
                if(os.path.getsize("requirements.txt") > 0):
                    reqFile.write("\n"+sys.argv[2])
                else:
                    reqFile.write(sys.argv[2])
            print "SystemDependencies installed successfully."
        else:
            shutil.rmtree(src)
            shutil.copytree(dst, src)
            print "SystemDependencies installation failed. Rolledback to previous state."
    else:
        shutil.rmtree(dst)
        print "Dependency already exisiting."

elif(sys.argv[1]=="uninstall"):
    try:
        fileData = open("requirements.txt","r")
        lines = fileData.readlines()
        fileData.close()
        tempName = None
        fileData = open("requirements.txt","w")
        for line in lines:
            if line.startswith(sys.argv[2]):
                tempName = line
            else:
                fileData.write(line)
        fileData.close()
        if(tempName):
            response = raw_input("Requirment File adjusted. It is required to remove from dependencies as well (Y/N): ")
            if(response=="Y"):
                shutil.rmtree(src)
                processOutput = subprocess.Popen('pip install --target='+depPath+' -r requirements.txt',shell=True,stderr=subprocess.PIPE)
                stdout, stderr = processOutput.communicate()
                if(stderr==None):
                    shutil.rmtree(dst)
                    print "SystemDependencies uninstalled successfully."
                else:
                    print stderr
                    shutil.copytree(dst, src)
                    shutil.rmtree(dst)
                    print "SystemDependencies uninstallation failed. Rolledback to previous state."

            else:
                shutil.rmtree(dst)
                print "SystemDependencies uninstalled successfully."
        else:
            shutil.rmtree(dst)
            print "No such dependency."
    except Exception as e:
        print e
        shutil.rmtree(src)
        shutil.copytree(dst, src)
        shutil.rmtree(dst)
