# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import re,os
from shutil import copyfile

compilerOptins =""
undefinedVariables = {}
undefinedInnerVariables = {}
analizerVariables = {}
reAnalizedVaraiables={}
parameterizedValues = []
parameterizedVariables = []
gloableValues = []
gloableNames = []
parameterNames = []
innerGlobales = []
fullGloableSet = ""
appendableFunction = ""
fileLocation = os.path.dirname(os.path.realpath(__file__))+"/Sandbox"
makeFileLocation = os.path.dirname(os.path.realpath(__file__))+"/Sandbox"


def makeObjectCode(fileName,makeFilePath):

    with open(makeFileLocation+makeFilePath, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('runnable', 'runnableILP')
    with open(makeFileLocation+makeFilePath, 'w') as file:
        file.write(filedata)

    processOutput = Popen('cd '+makeFileLocation +' && make && make clean ',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output,error=processOutput.communicate()
    if not "error" in error:
        copyfile(fileLocation+fileName,fileLocation+'finalCode.c')
        os.remove(fileLocation+fileName)
        copyfile(fileLocation+'originalCode.c',fileLocation+fileName)
        os.remove(fileLocation+'originalCode.c')
        return "success"
    else:
        return error


def createFinalSourceCode(fileName,loopStartLine,loopEndline):
    parameterSet =''
    for parameterizedValue in parameterizedVariables:
        if(parameterSet==''):
            parameterSet=parameterizedValue
        else:
            parameterSet = parameterSet+','+parameterizedValue
    globleString = ''
    for globalVar in gloableValues:
        if(globleString==''):
            globleString = globalVar.split(' ')[-1].split(';')[0]+' = '+globalVar.split(' ')[-1][8:]+'\n'
        else:
            globleString = globleString+''+globalVar.split(' ')[-1].split(';')[0]+ '='+globalVar.split(' ')[-1][8:]+'\n'

    globleReString = ''
    for globalVar in gloableValues:
        if(globleString==''):
            globleReString = globalVar.split(' ')[-1][8:]+' = '+globalVar.split(' ')[-1].split(';')[0]+'\n'
        else:
            globleReString = globleReString+''+globalVar.split(' ')[-1][8:].split(';')[0]+' = '+globalVar.split(' ')[-1]+'\n'

    reappendData = ''
    for innerglobalVar in innerGlobales:
        dataType = " ".join(innerglobalVar.split(' ')[:-1])
        if(reappendData==''):
            reappendData = dataType+" "+innerglobalVar.split(' ')[-1][8:].split(';')[0]+' = '+innerglobalVar.split(' ')[-1]+'\n'
        else:
            reappendData = reappendData+' '+ dataType+" "+innerglobalVar.split(' ')[-1][8:].split(';')[0]+' = '+innerglobalVar.split(' ')[-1]+'\n'
    addedHookFunction = False

    copyfile(fileLocation+fileName, fileLocation+'originalCode.c')
    os.remove(fileLocation+fileName)
    with open(fileLocation+'originalCode.c') as fin, open(fileLocation+fileName, 'w') as fout:
        for i, item in enumerate(fin, 1):
            if(i-loopStartLine==1):
                fout.write(globleString)
                fout.write('profileHook('+parameterSet+');exit(0); \n')
                fout.write(globleReString)
                fout.write(reappendData)
            if (i > loopStartLine) and (i < loopEndline) :
                continue
            else:
                if not addedHookFunction:
                    if '//----> AdditionalCodeHook' in item:
                        fout.write('//----> AdditionalCodeHook\n'+fullGloableSet+'\n'+appendableFunction+'\n')
                        addedHookFunction = True
                fout.write(item)

def addFunctionHook():
    parameterSet =''
    for parameterizedValue in parameterizedValues:
        if(parameterSet==''):
            parameterSet=parameterizedValue
        else:
            parameterSet = parameterSet+','+parameterizedValue
    reappendData = ''
    for innerglobalVar in innerGlobales:
        reappendData = reappendData+' '+innerglobalVar.split(' ')[-1].split(';')[0]+ '='+innerglobalVar.split(' ')[-1][8:].split(';')[0]+';'
    f = open(fileLocation+'target.c', "r")
    lines = f.readlines()
    f.close()
    profileHookStartLine = 0
    profileHookEndLine = 0
    for i, item in enumerate(lines):
        if  '/////######################################################/////' in item:
            newitem = item+'\n'+'void profileHook('+parameterSet+'){int iteratotConuter =0; \n'
            lines[i] = ''.join(newitem)
            profileHookStartLine = i
        if '/*addNewLoopPart*/break;' in item:
            newitem = item.replace("/*addNewLoopPart*/break;","/*dontErase*/iteratotConuter++; if(iteratotConuter>10){break;}; ",1)
            lines[i] = ''.join(newitem)
            profileHookEndLine = i
        if '/////----------------------------------------------------/////' in item:
            newitem = reappendData+'\n}'+'\n'+item
            lines[i] = ''.join(newitem)
            profileHookEndLine = i
    global appendableFunction
    appendableFunction = "".join(lines[profileHookStartLine:profileHookEndLine+1])

    f = open(fileLocation+'target.c', "w")
    f.write("".join(lines))
    f.close()


def addGlobaleDataSet():
    globleString = ' '
    for globalVar in gloableValues:
        globleString = globleString+' '+globalVar
    for innerglobalVar in innerGlobales:
        globleString = globleString+' '+innerglobalVar
    global fullGloableSet
    fullGloableSet = globleString
    f = open(fileLocation+'target.c', "r")
    lines = f.readlines()
    f.close()
    for i, item in enumerate(lines):
        if not 'include' in item:
            newitem = globleString+'\n'+item
            lines[i] = ''.join(newitem)
            break

    f = open(fileLocation+'target.c', "w")
    f.write("".join(lines))
    f.close()

def mapVariables():
    processOutput = Popen('clang -c -ferror-limit=1000 '+compilerOptins +' '+fileLocation+'target.c -o '+fileLocation+'target.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        line = processOutput.stderr.readline()
        if line != '':
            lineCode = line.rstrip()
            if('use of undeclared identifier' in lineCode):
                variable =  re.findall(r"'(.*?)'", lineCode, re.DOTALL)[0]
                if variable in gloableNames:
                    mapVariablesFixer()
                    break
            else:
                continue
        else:
            break

def mapVariablesFixer():
    processOutput = Popen('clang -c -ferror-limit=1000 '+compilerOptins +' '+fileLocation+'target.c -o '+fileLocation+'target.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        line = processOutput.stderr.readline()
        if line != '':
            lineCode = line.rstrip()
            if('use of undeclared identifier' in lineCode):
                variable =  re.findall(r"'(.*?)'", lineCode, re.DOTALL)[0]
                if variable in gloableNames:
                    lineNumber =  int(lineCode.split(':')[1])
                    charNumber = int(lineCode.split(':')[2])
                    f = open(fileLocation+'target.c', "r")
                    lines = f.readlines()
                    f.close()
                    for i, item in enumerate(lines):
                        if i==(lineNumber-1):
                            newitem = item[:charNumber-1]+'abcdefgh'+item[charNumber-1:]
                            lines[i] = ''.join(newitem)
                            break
                    f = open(fileLocation+'target.c', "w")
                    f.write("".join(lines))
                    f.close()
                    break
        else:
            break
    mapVariables()



def classifyPointers():
    for key in undefinedVariables.keys():
        if '(*)' in undefinedVariables[key]['type'] :
            tempParametercode = undefinedVariables[key]['type'].replace("(*)",key+'[]')
            parameterizedValues.append(tempParametercode)
            parameterizedVariables.append(key)
            parameterNames.append(key)
        elif '*' in undefinedVariables[key]['type'] :
            parameterizedValues.append(undefinedVariables[key]['type']+''+key)
            parameterizedVariables.append(key)
            parameterNames.append(key)
        else:
            gloableValues.append(undefinedVariables[key]['type']+' abcdefgh'+key+';')
            gloableNames.append(key)


def classifyInnerGloables():
    for key in undefinedInnerVariables.keys():
        innerGlobales.append(undefinedInnerVariables[key]['type']+' abcdefgh'+key+';')


#Identify the pointer variables in the code
def findInnerVariableTypeAttempt1(fileName,loopEndline):
    with open(fileLocation+fileName) as fin, open(fileLocation+'targetInnerChanged1.c', 'w') as fout:
        for i, item in enumerate(fin, 1):
            if i == loopEndline:
                for key in undefinedInnerVariables.keys():
                    item = 'printf("%p",'+key+');\n'+item
            fout.write(item)
    processOutput = Popen('clang -c '+compilerOptins +' '+fileLocation+'targetInnerChanged1.c -o '+fileLocation+'targetInnerChanged1.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        line = processOutput.stderr.readline()
        if line != '':
            lineCode = line.rstrip()
            if('warning:' in lineCode):
                variableType  = re.findall(r"'\s*([^']+?)\s*'", lineCode)[1]
                nextLine =  processOutput.stderr.readline()
                undefinedInnerVariables[re.search(r'\((.*?)\)',nextLine).group(1).split(',')[1]]['type'] = variableType

        else:
            break
def findInnerVariableTypeAttempt2(fileName,loopEndline):
    with open(fileLocation+fileName) as fin, open(fileLocation+'targetInnerChanged2.c', 'w') as fout:
        for i, item in enumerate(fin, 1):
            if i == loopEndline:
                for key in undefinedInnerVariables.keys():
                    item = 'printf("%f",'+key+');\n'+item
            fout.write(item)
    processOutput = Popen('clang -c '+compilerOptins +' '+fileLocation+'targetInnerChanged2.c -o '+fileLocation+'targetInnerChanged2.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        line = processOutput.stderr.readline()
        if line != '':
            lineCode = line.rstrip()
            if('warning:' in lineCode):
                variableType  = re.findall(r"'\s*([^']+?)\s*'", lineCode)[1]
                nextLine =  processOutput.stderr.readline()
                undefinedInnerVariables[re.search(r'\((.*?)\)',nextLine).group(1).split(',')[1]]['type'] = variableType

        else:
            break

#Identify the pointer variables in the code
def findVariableTypeAttempt1(fileName,loopStartLine):
    with open(fileLocation+fileName) as fin, open(fileLocation+'targetChanged1.c', 'w') as fout:
        for i, item in enumerate(fin, 1):
            if i == loopStartLine:
                for key in undefinedVariables.keys():
                    item = item + 'printf("%p",'+key+');\n'
            fout.write(item)
    processOutput = Popen('clang -c '+compilerOptins +' '+fileLocation+'targetChanged1.c -o '+fileLocation+'targetChanged1.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        line = processOutput.stderr.readline()
        if line != '':
            lineCode = line.rstrip()
            if('warning:' in lineCode):
                variableType  = re.findall(r"'\s*([^']+?)\s*'", lineCode)[1]
                nextLine =  processOutput.stderr.readline()
                undefinedVariables[re.search(r'\((.*?)\)',nextLine).group(1).split(',')[1]]['type'] = variableType

        else:
            break
def findVariableTypeAttempt2(fileName,loopStartLine):
    with open(fileLocation+fileName) as fin, open(fileLocation+'targetChanged2.c', 'w') as fout:
        for i, item in enumerate(fin, 1):
            if i == loopStartLine:
                for key in undefinedVariables.keys():
                    item = item + 'printf("%f",'+key+');\n'
            fout.write(item)
    processOutput = Popen('clang -c '+compilerOptins +' '+fileLocation+'targetChanged2.c -o '+fileLocation+'targetChanged2.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        line = processOutput.stderr.readline()
        if line != '':

            lineCode = line.rstrip()
            if('warning:' in lineCode):
                variableType  = re.findall(r"'\s*([^']+?)\s*'", lineCode)[1]
                nextLine =  processOutput.stderr.readline()
                undefinedVariables[re.search(r'\((.*?)\)',nextLine).group(1).split(',')[1]]['type'] = variableType

        else:
            break


def innerVaribales(fileName,loopStartLine,loopEndline):
    with open(fileLocation+fileName) as fin, open(fileLocation+'subTarget.c', 'w') as fout:
        for i, item in enumerate(fin, 1):
            if (i > loopStartLine) and (i < loopEndline) :
                continue
            else:
                fout.write(item)

    processOutput = Popen('clang -c -ferror-limit=1000 '+compilerOptins+' '+fileLocation+'subTarget.c -o '+fileLocation+'subTarget.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    nextLineUseful = False
    while True:
        line = processOutput.stderr.readline()
        if line != '':
            lineCode = line.rstrip()
            if(nextLineUseful):
                nextLineUseful = False
            if('use of undeclared identifier' in lineCode):
                nextLineUseful = True
                variable =  re.findall(r"'(.*?)'", lineCode, re.DOTALL)[0]

                if not variable in undefinedInnerVariables.keys():
                    undefinedInnerVariables[variable] = {
                        'type':'',
                        'dataSource':''
                    }
        else:
            break

def findVariables(fileName,loopStartLine,loopEndline):
    with open(fileLocation+fileName) as fin, open(fileLocation+'target.c', 'w') as fout:
        loopCount = 0;
        for i, item in enumerate(fin, 1):
            if '#include' in item:
                fout.write(item)
            if (i == loopStartLine):
                fout.write('int main() { \n /////######################################################///// \n')
            if (i > loopStartLine) and (i < loopEndline) :
                if ("}" in item) or ("{" in item):
                    loopCount = loopCount + len(item.split("{")) -len(item.split("}"))
                    if loopCount == 0:
                        item=item[::-1].replace("}","/*addNewLoopPart*/break;} ",1)
                fout.write(item)
            if (loopEndline - i == 1):
                fout.write(' /////----------------------------------------------------///// \n}')
    processOutput = Popen('clang -c -ferror-limit=1000 '+compilerOptins +' '+fileLocation+'target.c -o '+fileLocation+'target.o',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    nextLineUseful = False
    while True:
        line = processOutput.stderr.readline()
        if line != '':
            lineCode = line.rstrip()
            if(nextLineUseful):
                nextLineUseful = False
            if('use of undeclared identifier' in lineCode):
                nextLineUseful = True
                variable =  re.findall(r"'(.*?)'", lineCode, re.DOTALL)[0]

                if not variable in undefinedVariables.keys():
                    undefinedVariables[variable] = {
                        'type':'',
                        'dataSource':''
                    }
        else:
            break

def targetDataMapILP(fileName,makeFilePath,compilerOptinsPassed,loopStartLine,loopEndline):
    global compilerOptins
    compilerOptins =  compilerOptinsPassed
    global fileLocation
    fileLocation = fileLocation+fileName.rsplit('/', 1)[0]+"/"
    fileName = "/"+fileName.rsplit('/', 1)[1]
    global makeFileLocation
    makeFileLocation = makeFileLocation+makeFilePath.rsplit('/', 1)[0]+"/"
    makeFilePath = "/"+makeFilePath.rsplit('/', 1)[1]

    findVariables(fileName,loopStartLine,loopEndline)
    innerVaribales(fileName,loopStartLine,loopEndline)
    findVariableTypeAttempt1(fileName,loopStartLine)
    findVariableTypeAttempt2(fileName,loopStartLine)
    findInnerVariableTypeAttempt1(fileName,loopEndline)
    findInnerVariableTypeAttempt2(fileName,loopEndline)
    classifyPointers()
    classifyInnerGloables()
    addGlobaleDataSet()
    mapVariables()
    addFunctionHook()
    createFinalSourceCode(fileName,loopStartLine,loopEndline)
    result = makeObjectCode(fileName,makeFilePath)

    if (result == "success"):
    # Remove intermediate files
        os.remove(fileLocation+'target.c')
        os.remove(fileLocation+'subTarget.c')
        os.remove(fileLocation+'targetChanged2.c')
        os.remove(fileLocation+'targetChanged1.c')
        os.remove(fileLocation+'targetInnerChanged2.c')
        os.remove(fileLocation+'targetInnerChanged1.c')

    return result



#targetDataMap('profileCode.c',sys.argv[1],sys.argv[2],sys.argv[3],)
