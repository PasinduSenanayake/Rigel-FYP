import subprocess
import os
import shutil
import platform
import glob

def getBasicProfile(filePath,compTimeArguments="",runTimeArguments=""):
    response = {
        "error":"",
        "content":{},
        "returncode":0
        }
    try:
        if(os.path.isfile(filePath)):
            dirName = os.path.dirname(filePath)
            exisitingObjects = os.listdir(dirName)
            shutil.copy2(filePath, dirName+'/omppAnalysis.c')
            omppPath =  str(os.path.dirname(os.path.realpath(__file__)))+"/ompp/bin/kinst-ompp"
            omppPath2 = str(os.path.dirname(os.path.realpath(__file__)))+"/ompp/lib"
            if(platform.system() == "Linux"):
                temp_env = os.environ.copy()
                temp_env['OMPP_OUTFORMAT']='csv'
                temp_env['OMPP_APPNAME'] = 'omppAnalysis'
                processOutput = subprocess.Popen(omppPath+' gcc -L'+omppPath2+' -lompp -fopenmp '+ compTimeArguments +' omppAnalysis.c -o testapp',env=temp_env,shell=True, stderr=subprocess.PIPE,cwd=dirName)
                stdout, stderr = processOutput.communicate()
                if(stderr == ""):
                    processOutput = subprocess.Popen('./testapp '+str(runTimeArguments),env=temp_env,shell=True, stderr=subprocess.PIPE,cwd=dirName)
                    stdout, stderr = processOutput.communicate()
                    if(stderr == ""):
                        os.chdir(dirName)
                        csvFiles = glob.glob( '*.csv' )
                        matchedCSV = [csvFile for csvFile in csvFiles if "omppAnalysis" in csvFile]
                        if(len(matchedCSV)>0):
                            if(os.path.isfile(dirName+'/'+matchedCSV[0])):
                                with open(dirName+'/'+matchedCSV[0]) as fileData:
                                    response['content'] = fileData.readlines()
                                response['content'] = [element.replace("\n", "") for element in response['content']]
                                response['returncode']=1
                            else:
                                response['error']="Ompp failed Process terminated. Please check your input file."
                                response['returncode']=0
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

            allExisitingObjects = os.listdir(dirName)
            newlyAddedObjects = list(set(allExisitingObjects) - set(exisitingObjects))
            for newlyAddedObject in newlyAddedObjects:
                if(os.path.isfile(dirName+'/'+newlyAddedObject)):
                    os.remove(dirName+'/'+newlyAddedObject)
                elif(os.path.isdir(dirName+'/'+newlyAddedObject)):
                    shutil.rmtree(dirName+'/'+newlyAddedObject)
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
