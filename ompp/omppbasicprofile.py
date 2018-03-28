import subprocess
import os
import shutil
import platform

def getBasicProfile(filePath, arguments=""):
    response = {
        "error":"",
        "content":{},
        "returncode":0
        }
    try:
        if(os.path.isfile(filePath)):
            shutil.copy2(filePath, os.getcwd()+'/test.c')
            omppPath =  str(os.path.dirname(os.path.realpath(__file__)))+"/ompp/bin/kinst-ompp"
            omppPath2 = str(os.path.dirname(os.path.realpath(__file__)))+"/ompp/lib"
            if(platform.system() == "Linux"):
                temp_env = os.environ.copy()
                temp_env['OMPP_OUTFORMAT']='csv'
                processOutput = subprocess.Popen(omppPath+' gcc -L'+omppPath2+' -lompp -fopenmp test.c -o testapp',env=temp_env,shell=True, stderr=subprocess.PIPE)
                stdout, stderr = processOutput.communicate()
                if(stderr == ""):
                    processOutput = subprocess.Popen('./testapp '+str(arguments),env=temp_env,shell=True, stderr=subprocess.PIPE)
                    stdout, stderr = processOutput.communicate()
                    if(stderr == ""):
                        if(os.path.isfile('unknown.4-0.ompp.csv')):
                            with open('unknown.4-0.ompp.csv') as fileData:
                                response['content'] = fileData.readlines()
                            response['content'] = [element.replace("\n", "") for element in response['content']]
                            response['returncode']=1
                        else:
                            response['error']="Ompp failed Process terminated. Please check your input file."
                            response['returncode']=0
                    else:
                        print stderr
                        response['error']="Run time error occured in C file."
                        response['returncode']=0
                else:
                    print stderr
                    response['error']="Compiler time error occured in C file"
                    response['returncode']=0

            else:
                response['error']="Incompatiable platform"
                response['returncode']=0

            if(os.path.isfile('test.c')):
                os.remove('test.c')
            if(os.path.isfile('test.c.opari.inc')):
                os.remove('test.c.opari.inc')
            if(os.path.isfile('test.mod.c')):
                os.remove('test.mod.c')
            if(os.path.isfile('opari.rc')):
                os.remove('opari.rc')
            if(os.path.isfile('opari.tab.c')):
                os.remove('opari.tab.c')
            if(os.path.isfile('opari.tab.o')):
                os.remove('opari.tab.o')
            if(os.path.isfile('testapp')):
                os.remove('testapp')
            if(os.path.isfile('unknown.4-0.ompp.csv')):
                os.remove('unknown.4-0.ompp.csv')
        else:
            response['error']="Input file path doesn't contain a C file."
            response['returncode']=0
    except Exception as e:
        print e
        print "Unexpected Error Occured."
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
    return response
