# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import re,os
from Tkinter import *

undefinedVariables = {}
operationArray = ['+=','-=','*=','/=','%=']
directoryPath = ""
#Show extracted data and get approval from user to proceed
def getUserApproval():
    optionValSet = []
    desValSet = []
    keySet = []
    for key in undefinedVariables.keys():
        keySet.append(key)
        optionValSet.append(undefinedVariables[key]['type'])
        desValSet.append('0')
    rowlength = len(undefinedVariables.keys())
    def buttonClick():
        for index,key in enumerate(keySet):
            undefinedVariables[key]['type'] = optionValSet[index].get()
            undefinedVariables[key]['dataSource'] = key+desValSet[index].get()
        window.destroy()

    #UI Elements
    window = Tk()
    window.title("GPU Offloading Data Mapper")
    window.geometry('500x'+str(30*rowlength + 60))
    lbl = Label(window, text="Pointer Map")
    lbl.grid(column=1, row=0, pady=(2, 10))
    lbl = Label(window, text="Map Type")
    lbl.grid(column=4, row=0, pady=(2, 10))
    for i in range (0,rowlength,1):
        lbl = Label(window, text=str(i+1)+".")
        lbl.grid(column=0, row=(i+2))
        lbl = Label(window, text=keySet[i])
        lbl.grid(column=1, row=(i+2))
        desValSet[i] = StringVar()
        txt = Entry(window,width=10)
        txt.grid(column=2, row=(i+2))
        txt.config(textvariable=desValSet[i])
        optionValSet[i] = StringVar(None, optionValSet[i])
        rad1 = Radiobutton(window,text='To', value='to',var=optionValSet[i])
        rad2 = Radiobutton(window,text='From', value='from', var=optionValSet[i])
        rad3 = Radiobutton(window,text='ToFrom', value='tofrom', var=optionValSet[i])
        rad4 = Radiobutton(window,text='Alloc', value='alloc',var=optionValSet[i])
        rad1.grid(column=3, row=(i+2))
        rad2.grid(column=4, row=(i+2))
        rad3.grid(column=5, row=(i+2))
        rad4.grid(column=6, row=(i+2))
    btn = Button(window, text="Mapped",command=buttonClick)
    btn.grid(column=3, row=(rowlength+4),pady=(20, 0))
    window.mainloop()


def findVariableMappingType():
    processOutput = Popen('clang -ferror-limit=1000 '+directoryPath+'/target.c -o testCpu',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    nextLineUseful = False
    while True:
        line = processOutput.stderr.readline()
        if line != '':
            lineCode = line.rstrip()
            if('use of undeclared identifier' in lineCode):
                variable =  re.findall(r"'(.*?)'", lineCode, re.DOTALL)[0]
                lineCode = processOutput.stderr.readline().rstrip()
                charPos = processOutput.stderr.readline().rstrip().index('^')
                if variable in undefinedVariables.keys():
                    if '++' in lineCode:
                        undefinedVariables[variable]['nature']['read'] = True
                        undefinedVariables[variable]['nature']['write'] = True
                    if '--' in lineCode:
                        undefinedVariables[variable]['nature']['read'] = True
                        undefinedVariables[variable]['nature']['write'] = True
                    for operation in operationArray:
                        if(operation in lineCode):
                            if lineCode.index(operation) > charPos:
                                undefinedVariables[variable]['nature']['read'] = True
                                undefinedVariables[variable]['nature']['write'] = True
                            else:
                                undefinedVariables[variable]['nature']['read'] = True
                    if lineCode.count('=') ==1:
                        if lineCode.index('=') > charPos:
                            undefinedVariables[variable]['nature']['write'] = True
                        else:
                            undefinedVariables[variable]['nature']['read'] = True
        else:
            break
    # Identify the variable type
    for key in undefinedVariables.keys():
        if (undefinedVariables[key]['nature']['read'] and undefinedVariables[key]['nature']['write']):
            undefinedVariables[key]['type']='tofrom'
        else:
            if (undefinedVariables[key]['nature']['read']):
                undefinedVariables[key]['type']='to'
            if (undefinedVariables[key]['nature']['write']):
                undefinedVariables[key]['type']='from'


def findVariableType(path,loopStartLine):
    with open(path) as fin, open(directoryPath + '/targetChanged.c', 'w') as fout:
        for i, item in enumerate(fin, 1):
            if i == loopStartLine:
                for key in undefinedVariables.keys():
                    item = item + 'printf("%d",'+key+');\n'
            fout.write(item)
    processOutput = Popen('clang -fopenmp -ferror-limit=1000 '+ directoryPath+'/targetChanged.c -o testCpu',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        line = processOutput.stderr.readline()
        if line != '':
            lineCode = line.rstrip()
            if('warning:' in lineCode):
                variableType  = re.findall(r"'\s*([^']+?)\s*'", lineCode)[1]
                nextLine =  processOutput.stderr.readline()
                if not '*' in variableType :
                    del undefinedVariables[re.search(r'\((.*?)\)',nextLine).group(1).split(',')[1]]
                else:
                    undefinedVariables[re.search(r'\((.*?)\)',nextLine).group(1).split(',')[1]]['pointer'] = True
        else:
            break
    for key in undefinedVariables.keys():
        if not (undefinedVariables[key]['pointer']):
            del undefinedVariables[key]


def mapTargetData(path,loopStartLine,loopEndline):
    global undefinedVariables
    undefinedVariables = {}
    global directoryPath
    fileName = path.split("/")[-1]
    directoryPath = path.replace("/"+fileName,"")

    with open(path) as fin, open(directoryPath+'/target.c', 'w') as fout:
        for i, item in enumerate(fin, 1):
            if 'include' in item:
                fout.write(item)
            if (i == loopStartLine):
                fout.write('int main() { \n')
            if (i > loopStartLine) and (i < loopEndline) :
                fout.write(item)
            if (loopEndline - i == 1):
                fout.write('}')
    processOutput = Popen('clang -ferror-limit=1000 ' + directoryPath + '/target.c -o testCpu',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
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
                    nature = {
                        'read':False,
                        'write':False,
                    }
                    undefinedVariables[variable] = {
                        'nature': nature,
                        'pointer':False
                    }
        else:
            break
    findVariableType(path,loopStartLine)
    findVariableMappingType()
    getUserApproval()
    pragma = '#pragma omp target data'
    for key in undefinedVariables.keys():
        if (undefinedVariables[key]['nature']['read'] and undefinedVariables[key]['nature']['write']):
            pragma  = pragma + ' map(tofrom:'+ undefinedVariables[key]['dataSource'] +')'
        else:
            if (undefinedVariables[key]['nature']['read']):
                pragma  = pragma + ' map(to:'+ undefinedVariables[key]['dataSource'] + ')'
            if (undefinedVariables[key]['nature']['write']):
                pragma  = pragma + ' map(from:'+ undefinedVariables[key]['dataSource'] + ')'
    os.remove(directoryPath+'/target.c')
    os.remove(directoryPath+'/targetChanged.c')
    return pragma
