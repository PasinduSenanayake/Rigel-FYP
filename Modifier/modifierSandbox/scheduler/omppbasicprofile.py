import subprocess
import os
import shutil
import platform
import glob

def getBasicProfile(dirPath,runTimeArguments=""):
    response = {
        "error":"",
        "content":{},
        "returncode":0
        }
    try:
        if(os.path.isdir(dirPath)):
            if(os.path.isdir(str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")):
                shutil.rmtree(str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")
            shutil.copytree(dirPath, str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")
            omppPath =  str(os.path.dirname(os.path.realpath(__file__)))+"/ompp/bin/kinst-ompp"
            omppPath2 = str(os.path.dirname(os.path.realpath(__file__)))+"/ompp/lib"
            lines =[]
            with open(str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox/Makefile") as books:
                lines = books.readlines()
                for index,line in enumerate(lines):
                    if '[compiler]' in line:
                        line = line.replace("[compiler]",omppPath+' clang -L'+omppPath2+' -lompp -fopenmp')
                        lines[index] = line
                    if '[targetObject]' in line:
                        line = line.replace("[targetObject]",'testapp')
                        lines[index] = line
            with open(str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox/Makefile", 'w') as rewriteMake:
                rewriteMake.writelines(lines)
            temp_env = os.environ.copy()
            temp_env['OMPP_OUTFORMAT']='csv'
            temp_env['OMPP_APPNAME'] = 'omppAnalysis'
            processOutput = subprocess.Popen('make',env=temp_env,shell=True, stderr=subprocess.PIPE,cwd=str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")
            stdout, stderr = processOutput.communicate()
            if(stderr == ""):
                processOutput = subprocess.Popen(os.path.dirname(os.path.realpath(__file__))+'/sandbox/testapp '+str(runTimeArguments),env=temp_env,shell=True, stderr=subprocess.PIPE,cwd=str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")
                stdout, stderr = processOutput.communicate()
                if(stderr == ""):
                    os.chdir(os.path.dirname(os.path.realpath(__file__))+"/sandbox")
                    csvFiles = glob.glob( '*.csv' )
                    matchedCSV = [csvFile for csvFile in csvFiles if "omppAnalysis" in csvFile]
                    if(len(matchedCSV)>0):
                        if(os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/sandbox"+'/'+matchedCSV[0])):
                            with open(os.path.dirname(os.path.realpath(__file__))+"/sandbox"+'/'+matchedCSV[0]) as fileData:
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
            shutil.rmtree(str(os.path.dirname(os.path.realpath(__file__)))+"/sandbox")
        else:
            response['error']="Provided Path is not a directory"
            response['returncode']=0
    except Exception as e:
        print e
        print "Unexpected Error Occured."
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
    return response
