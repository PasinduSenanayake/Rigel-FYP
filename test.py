
#
# import ompp
# import os
#
#
# temp = ompp.getBasicProfile(os.getcwd()+"/foo.c",2)
# print temp["content"]
import os
import subprocess
import sys
del sys.path[0:len(sys.path)]
# sys.path.append('dsdsds')
processOutput = subprocess.Popen('pip freeze -l > req.txt',shell=True, stderr=subprocess.PIPE)
stdout, stderr = processOutput.communicate()
print sys.path
