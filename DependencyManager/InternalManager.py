import json
import os
import shutil

filesPath = str(os.path.dirname(os.path.realpath(__file__)))


shutil.copy2(filesPath+'/requirements.json', filesPath+'/tmprequirements.json')
shutil.copy2(filesPath+'/requirementsLocal.json', filesPath+'/tmprequirementsLocal.json')
shutil.copy2(filesPath+'/requirements.txt', filesPath+'/tmprequirements.txt')


def removeTemp():
    os.remove(filesPath+'/tmprequirements.json')
    os.remove(filesPath+'/tmprequirementsLocal.json')
    os.remove(filesPath+'/tmprequirements.txt')

def reverseback():
    shutil.copy2(filesPath+'/tmprequirements.json', filesPath+'/requirements.json')
    shutil.copy2(filesPath+'/tmprequirementsLocal.json', filesPath+'/requirementsLocal.json')
    shutil.copy2(filesPath+'/tmprequirements.txt', filesPath+'/requirements.txt')

def moduleCheck(module,version):
    response = {
        "error":"",
        "info":"",
        "code":0
        }
    try:
        with open(filesPath+'/requirements.json') as json_data:
            requirements = json.load(json_data)

        if module in requirements['Dependencies']:
            if(requirements['Dependencies'][module] == version):
                response['info'] = "Module is already there"
                response['code'] = 1
            else:
                response['info']= "Module will be upgraded to the given version"
                response['code'] = 2
        else:
            response['info'] = "Module will be installed"
            response['code'] = 3
    except Exception as error:
        response['info'] = ""
        response['error'] = error
        response['code'] = 0
    return response

def moduleUpdateCheck(module,version):
    response = {
        "error":"",
        "info":"",
        "code":0
        }
    try:
        with open(filesPath+'/requirementsLocal.json') as json_data:
            requirements = json.load(json_data)

        if module in requirements['Dependencies']:
            if(requirements['Dependencies'][module] == version):
                response['info'] = "Module is already there"
                response['code'] = 1
            else:
                response['info']= "Module will be upgraded to the given version"
                response['code'] = 2
        else:
            response['info'] = "Module will be installed"
            response['code'] = 3
    except Exception as error:
        response['info'] = ""
        response['error'] = error
        response['code'] = 0
    return response

def updateMain(opertation,module,version=""):
    response = {
        "error":"",
        "info":"",
        "code":0
        }
    try:
        with open(filesPath+'/requirements.json') as json_data:
            requirements = json.load(json_data)
        if(opertation=="update"):
            requirements['Dependencies'][module] = version
            response['info'] = "Module upgraded successfully."
        elif(opertation=="install"):
            requirements['Dependencies'][module] = version
            response['info'] = "Module installed successfully."
        elif(opertation=="uninstall"):
            del requirements['Dependencies'][module]
            response['info'] = "Module uninstalled successfully."
        response['code'] = 1
        response['error'] = ""
        with open(filesPath+'/requirements.json', 'w') as json_file:
            json.dump(requirements, json_file)
    except Exception as error:
        response['info'] = ""
        response['error'] = error
        response['code'] = 0
    return response


def updateLocal():
    response = {
        "error":"",
        "info":"",
        "code":0
        }
    try:
        shutil.copyfile(filesPath+'/requirements.json', filesPath+'/requirementsLocal.json')
        response['info'] = "Local Json updated successfully."
        response['code'] = 1
        response['error'] = ""
    except Exception as error:
        response['info'] = ""
        response['error'] = error
        response['code'] = 0
    return response

def updateRequirementFile():
    response = {
        "error":"",
        "info":"",
        "code":0
        }
    try:
        with open(filesPath+'/requirements.json') as json_data:
            requirements = json.load(json_data)
        with open(filesPath+'/requirements.txt', 'w') as reqFile:
            for dependencyKey in requirements['Dependencies'].keys():
                tempString = dependencyKey+"=="+requirements['Dependencies'][dependencyKey]
                reqFile.write(tempString + os.linesep)
        response['info'] = "Requirements file updated successfully."
        response['code'] = 1
        response['error'] = ""
    except Exception as error:
        response['info'] = ""
        response['error'] = error
        response['code'] = 0
    return response

def updateCheck():
    response = {
        "error":"",
        "info":{"install":{},"upgrade":{}},
        "code":0
        }
    try:
        with open(filesPath+'/requirements.json') as json_data:
            requirements = json.load(json_data)
        with open(filesPath+'/requirementsLocal.json') as json_data:
            requirementsLocal = json.load(json_data)
        for req in requirements['Dependencies'].keys():
            if req in requirementsLocal['Dependencies'].keys():
                if not requirementsLocal['Dependencies'][req] == requirements['Dependencies'][req]:
                    response['info']['upgrade'][req] = requirements['Dependencies'][req]
            else:
                response['info']['install'][req] = requirements['Dependencies'][req]
        response['code'] = 1
        response['error'] = ""
    except Exception as error:
        response['info'] = {}
        response['error'] = error
        response['code'] = 0
    return response
