import sys
import subprocess
import os
import shutil

depPath = str(os.path.dirname(os.path.realpath(__file__)))+"/Utils"
try:
    if(os.path.isdir(depPath)):
        shutil.rmtree(depPath)
    os.makedirs(depPath)
    processOutput = subprocess.Popen('pip install --target='+depPath+' -r DependencyManager/requirements.txt',shell=True)
    stdout, stderr = processOutput.communicate()
    if(stderr==None):
        print "Modules installed successfully."
    else:
        print stderr
        shutil.rmtree(depPath)
        print "Modules installation failed."
except Exception as e:
    print e
    print "Modules installation failed."
    shutil.rmtree(depPath)
