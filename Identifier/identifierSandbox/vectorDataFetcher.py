from Identifier.identifierSandbox.nonArchiFeatureFetcher.vectorSourceAnnotatorBranch import targetDataMapBranch
import subprocess
from subprocess import Popen, PIPE
import os
import shutil

def vtuneProfiler(codeName,mainFilePath,annotatedFile,makeFile,compileCommand,arguments,segmentArray,initLocation,trainCollection=True):
    # print(codeName,mainFilePath,annotatedFile,makeFile,compileCommand,arguments,segmentArray,initLocation)
    location = initLocation+'/Sandbox'
    runfile = location+'/runnableTest'
    targetDataMapBranch(annotatedFile, makeFile, '', segmentArray[0][0], segmentArray[0][1])
    profile_command = "cd /opt/intel/vtune_amplifier/bin64/ && ./amplxe-cl -collect general-exploration -knob sampling-interval=10 -result-dir " + location +"/temp"+str(segmentArray[0][0])+ " " + runfile
    report_command = "cd /opt/intel/vtune_amplifier/bin64/ && ./amplxe-cl -report hw-events -format csv -csv-delimiter comma -result-dir "+ location +"/temp"+str(segmentArray[0][0])+" -report-output "+initLocation+"/"+codeName+".csv "
    print(profile_command)
    profileprocessOutput = Popen(profile_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, error1 = profileprocessOutput.communicate()

    reportprocessOutput = Popen(report_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, error2 = reportprocessOutput.communicate()

    # os.system(command)
    # process.wait()
    print(error1)
    print(error2)
    # print(output)



