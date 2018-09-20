import subprocess
import os
import json

response = {
    "returncode":0,
    "error":"",
    "content":{}
}

inputfilepath = str(os.path.dirname(os.path.realpath(__file__))) +os.sep +"SystemDependencies"+os.sep + "command.json"
outputFilepath =str(os.path.dirname(os.path.realpath(__file__))) + os.sep +"sysinfo"+os.sep + "systemInfo.json"
hwdFilepath = str(os.path.dirname(os.path.realpath(__file__))) +os.sep +"SystemDependencies"+os.sep + "storage.json"
deviceQueryPath = str(os.path.dirname(os.path.realpath(__file__))) +os.sep +"SystemDependencies"+os.sep + "deviceQuery.cpp"

NVIDIA_TAG = "NVIDIA"
DEVICE_QUERY_END_ATTRIBUTE = "Maximum number of threads per block"
NVIDIA_NVCC_COMMAND = "nvcc " + deviceQueryPath + " -o deviceQuery && ./deviceQuery "

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
               "cpu_average_speed":"",
               "architecture":""}
gpu_info_list={}

nvidia_info_list = {"compute_capability":"",
                    "warp_size":"",
                    "num_SM":"",
                    "cuda_cores_per_SM":"",
                    "global_memory":"",
                    "L2_cache":"",
                    "constant_memory":"",
                    "shared_memory_per_block":"",
                    "registers_per_block":"",
                    "max_threads_per_block":""}

systemInforDictionary = {"cpuinfo":cpu_info_list,
                       "gpuinfo":gpu_info_list}

# dictionary used to map json mapping attribute names with system hardware details
cpu_json_mapping={"Core(s) per socket":"num_cores",
                  "Thread(s) per core":"threads_per_core",
                  "L1d cache":"cache_L1_data",
                  "L1i cache":"cache_L1_inst",
                  "L2 cache":"cache_L2",
                  "L3 cache":"cache_L3",
                  "Model name":"model_name",
                  "CPU max MHz":"cpu_max_speed",
                  "Flags":"vectorization",
                  "Architecture": "architecture"}

gpu_json_mapping={"VGA compatible controller":"VGAinfo",
                  "3D controller":"3Dcontrollerinfo"}

# dictionary used to map nvidia GPU device query output to accelerator details
nvidia_json_mapping ={"CUDA Capability Major/Minor version number":"compute_capability",
                      "Multiprocessors":"num_SM",
                      "CUDA Cores/MP":"cuda_cores_per_SM",
                      "Warp size":"warp_size",
                      "Total amount of global memory":"global_memory",
                      "L2 Cache Size":"L2_cache",
                      "Total amount of constant memory":"constant_memory",
                      "Total amount of shared memory per block":"shared_memory_per_block",
                      "Total number of registers available per block":"registers_per_block",
                      "Maximum number of threads per block":"max_threads_per_block"}

systemCommandDictionary = {}

hdwInfoDictionary = {}

deviceCount = 0

# function can be used to organize stdoutput from shell output
def __extractCpuInformation(sysoutput):
    global cpu_info_list
    list_output = sysoutput.splitlines()
    for x in cpu_json_mapping:
        for y in list_output:
            if x in y:
                cpu_info_list[cpu_json_mapping[x]] = y.split(":")[1].strip()
                break


def __extracGpuInformation(sysoutput,key):
    global gpu_info_list
    global deviceCount
    list_output = sysoutput.splitlines()
    for acc in list_output:
        if key in acc:
            s = acc.split(":")[2].strip()

            if NVIDIA_TAG in s:
                deviceCount = deviceCount + 1

# function can be used to extract extra details from original details
def __extractDetails(value,splitCharacter,key):
    global cpu_info_list
    cpu_info_list[key]=value.split(splitCharacter)[1].strip()


def __extractVectorizationinfo():
    global hdwInfoDictionary
    global cpu_info_list

    architecture = cpu_info_list["architecture"].split("_")[0]  # will work only for x86 architectures
    instructionset_list = hdwInfoDictionary["vectorization"][architecture]
    tempFlag_list = cpu_info_list["vectorization"].split()
    vector_inst_list = []
    for inst in instructionset_list:
        if inst.lower() in [flag.lower() for flag in tempFlag_list]:
            vector_inst_list.append(inst.lower())
    cpu_info_list["vectorization"] = vector_inst_list



def __extractNvidiaGPUinfo():
    global nvidia_info_list
    global gpu_info_list

    if deviceCount > 0:
        p = subprocess.Popen(NVIDIA_NVCC_COMMAND , shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (output, err) = p.communicate() #to check for errors
        if len(err) == 0:
            deviceQuery_list = output.splitlines()
            detect = int(deviceQuery_list[0].split('=')[1])

            for gpu in range(0 , detect):
                name_='Device_'+str(gpu)
                start, end = index_containing_substring(deviceQuery_list, name_, DEVICE_QUERY_END_ATTRIBUTE)
                gpu_model = deviceQuery_list[start].split(':')[1]
                if start is not -1:
                     temp_list = deviceQuery_list[start:end]
                     for key in nvidia_json_mapping:
                         for value in temp_list:
                             if key in value:
                                 nvidia_info_list[nvidia_json_mapping[key]] = value.split(":")[1].strip()
                                 break
                     deviceQuery_list = deviceQuery_list[end:]
                     gpu_info_list[gpu_model] = nvidia_info_list

        else:
            response['error'] = err
            response['content'] = {}
            response['returncode'] = 0
            return response


def index_containing_substring(the_list, substring,substring2):
    start_index = -1
    end_index = -1
    for start, s in enumerate(the_list):
        if substring in s:
              start_index = start
              break
    for end, s in enumerate(the_list[start_index:]):
        if substring2 in s:
            end_index =start_index + end + 1
            break
    return start_index, end_index


def __systemInformationIdentifier():
    global systemCommandDictionary
    global hdwInfoDictionary
    try:
        with open(inputfilepath) as inputfile:
            systemCommandDictionary = json.load(inputfile)
        with open(hwdFilepath) as hdwinfoFile:
            hdwInfoDictionary = json.load(hdwinfoFile)
    except Exception as e:
            response['error'] = str(e)
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
                __extractVectorizationinfo()
            elif infocmd == "VGAinfo":
                __extracGpuInformation(output, "VGA compatible controller")
            elif infocmd == "3Dcontrollerinfo":
                __extracGpuInformation(output,"3D controller")
            __extractNvidiaGPUinfo() #extract nvidia gpu information finally
        except Exception as e:
            response['error'] = e
            response['content'] = {}
            response['returncode'] = 0
            return response

    try:

        with open(outputFilepath, 'w') as outfile:
            json.dump(systemInforDictionary, outfile)
        response['returncode'] = 1
        response['error'] = ""
        response['content'] = systemInforDictionary
    except Exception as e:
        response['error'] = e
        response['content'] = {}
        response['returncode'] = 0
    finally:
        return response
