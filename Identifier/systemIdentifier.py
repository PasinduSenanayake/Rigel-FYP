import subprocess
import os
import json


response = {
    "returncode":0,
    "error":"",
    "content":{}
}

# dictionary used to map data to Json information holder
cpu_info_list={"num_cores":"",
               "threads_per_core":"",
               "cache_L1_data":"",
               "cache_L1_inst":"",
               "cache_L2":"",
               "cache_L3":"",
               "model_name":"",
               "cpu_max_speed":"",
               "vectorization":"",
               "cpu_average_speed":""}

# dictionary used to map json mapping attribute names with system hardware details
cpu_json_mapping={"Core(s) per socket":"num_cores",
                  "Thread(s) per core":"threads_per_core",
                  "L1d cache":"cache_L1_data",
                  "L1i cache":"cache_L1_inst",
                  "L2 cache":"cache_L2",
                  "L3 cache":"cache_L3",
                  "Model name":"model_name",
                  "CPU max MHz":"cpu_max_speed",
                  "Flags":"vectorization"}

gpu_json_mapping={"VGA compatible controller":"VGAinfo",
                  "3D controller":"3Dcontrollerinfo"}

gpu_info_list={"VGAinfo":[],"3Dcontrollerinfo":[]}

systemInforDictionary = {"cpuinfo":cpu_info_list,
                        "gpuinfo":gpu_info_list}

systemCommandDictionary = {}

inputfilepath = str(os.path.dirname((os.path.dirname(os.path.realpath(__file__))))) + os.sep +"SystemDependencies"+os.sep + "command.json"
outputFilepath =str(os.path.dirname(os.path.realpath(__file__))) + os.sep +"sysinfo"+os.sep + "systemInfo.json"


# function can be used to organize stdoutput from shell output
def __extractCpuInformation(sysoutput):
    list_output = sysoutput.splitlines()
    for x in cpu_json_mapping:
        for y in list_output:
            if x in y:
                cpu_info_list[cpu_json_mapping[x]] = y.split(":")[1].strip()
                break


def __extracGpuInformation(sysoutput,key):
    list_output = sysoutput.splitlines()
    for acc in list_output:
        if key in acc:
            tempList = gpu_info_list[gpu_json_mapping[key]]
            tempList.append(acc.split(":")[2].strip())
            gpu_info_list[gpu_json_mapping[key]] = tempList


# function can be used to extract extra details from original details
def __extractDetails(value,splitCharacter,key):
    cpu_info_list[key]=value.split(splitCharacter)[1].strip()


def __systemInformationIdentifier():
    try:
        with open(inputfilepath) as inputfile:
            systemCommandDictionary = json.load(inputfile)
    except Exception as e:
            response['error'] = e
            response['content'] = {}
            response['returncode'] = 0
            return response

    for infocmd in systemCommandDictionary["Linux"]["info"]:
        try:
            p = subprocess.Popen(systemCommandDictionary["Linux"]["info"][infocmd], shell=True, stdout=subprocess.PIPE)
            (output, err) = p.communicate()
            if infocmd == "cpuinfo":
                __extractCpuInformation(output)
                __extractDetails(cpu_info_list["model_name"], "@", "cpu_average_speed")
            elif infocmd == "VGAinfo":
                __extracGpuInformation(output, "VGA compatible controller")
            elif infocmd == "3Dcontrollerinfo":
                __extracGpuInformation(output,"3D controller")
        except Exception as e:
            response['error'] = e
            response['content'] = {}
            response['returncode'] = 0
            return response

    try:
        with open(outputFilepath, 'w') as outfile:
            json.dump(systemInforDictionary, outfile)
        response['returncode'] = 1
        print response['returncode']
        response['error'] = ""
        response['content'] = "System Data Fetcher successfully executed"
    except Exception as e:
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
    finally:
        return response
