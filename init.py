import sys
import platform
import json
import subprocess
import os
import shutil

depPath = os.getcwd()+"/Utils"
processOutput = subprocess.Popen('python -m pip install --target='+depPath+' -r requirements.txt',shell=True)
stdout, stderr = processOutput.communicate()
if(stderr==None):
    print "SystemDependencies installed successfully."
else:
    print stderr
    shutil.rmtree(depPath)
    print "SystemDependencies installation failed."

# with open('SystemDependencies/command.json') as json_data:
#     d = json.load(json_data)
# sys.path.append(subprocess.check_output([d[platform.system()]['pathFinder']]).strip('\n')+"/Utils")
sys.path.append(depPath)
import paramiko
sys.path.remove(depPath)
