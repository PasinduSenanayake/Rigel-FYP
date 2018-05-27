import os
import sys
import argparse
from subprocess import Popen, PIPE
import re
from Loop import Loop
from FileHandler import FileHandler


sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Utils")

parser = argparse.ArgumentParser(description='Initilizer of analyzer')
parser.add_argument('-fp', '--fpath', type=str, help='Absolute file path', required=False)
parser.add_argument('-ca', '--carguments', type=str, help='Compiler time arguments', required=False, default="")
parser.add_argument('-fa', '--farguments', type=str, help='Run time arguments', required=False, default="")
args = parser.parse_args()
response = {
    "returncode":0,
    "error":"",
    "content":{}
    }
arguments = {
    "fileAbsPath":args.fpath,
    "runTimeArguments":args.farguments,
    "compTimeArguments":args.carguments
    }

class VectorReportAnaLyzer:
    def __init__(self):
        self.source = ''
        self.vectors = {}

    def addSource(self, sourcePath):
        self.source = sourcePath
    def compileFile(self):
        command = 'icc -o2 -qopt-report=5 -qopt-report-phase=all '+self.source
        print(command)
        processOutput = Popen(command,shell=True)
        stdout, stderr = processOutput.communicate()
        if(stderr==None):
            print "Compiled Successfully"
        else:
            print stderr

    def getFileName(self):
        fullname=self.source.split("/")[-1]
        # print(fullname)
        return fullname

    def readVectorReport(self,filename):
        file = FileHandler.getInstance().readSource(filename[0:-2]+'.optrpt')
        # print("read")
        return file

    def getVectorData(self,lineNo, report ):
        line = 0;
        vectorLen = 0 ;
        speedup = 0 ;
        lineregex = re.compile(r"LOOP BEGIN", re.DOTALL)
        vectorLenregex = re.compile(r"#15305")
        speedupregex = re.compile(r"#15478")
        for i in range(lineNo,0,-1):
            match1 = lineregex.search(report[i])
            match2 = vectorLenregex.search(report[i])
            if match2:
                fullLine = report[i][:-1]
                filter(str.isalnum, fullLine)
                vectorLen = int(fullLine[-1:])
            if match1:
                val =report[i].split('(', 1)[1].split(')')[0]
                line = int(val.split(',')[0])
                break
        for i in range(lineNo,len(report),1):
            match3 = speedupregex.search(report[i])
            if match3:
                fullLine = report[i][:-1]
                speedup = fullLine.split(':')[-1].split(' ')[1]
                break
        # print(str(line)+" "+str(vectorLen)+" "+str(speedup))
        loop = Loop(line,vectorLen,speedup)
        return loop

    def findLoopBlocks(self,report):
        vectorDataList= []
        for i in range(0,len(report)):
            regex1 = re.compile(r"#15300", re.DOTALL)
            match = regex1.search(report[i])
            regex2 = re.compile(r"#15301", re.DOTALL)
            match1 = regex2.search(report[i])
            if match or match1:
                vectorData = self.getVectorData(i,report)
                if vectorData not in vectorDataList :
                    vectorDataList.append(vectorData)
        return vectorDataList

    def removeDuplicateLoops(self,loopList):
        duplicateList = []
        for vector1 in loopList:
            duplicateList.append(vector1)
            count =0
            for vector2 in duplicateList:
                if vector1.line == vector2.line:
                    count +=1
                if count >1 :
                    duplicateList.pop()
        return duplicateList

    def execute(self):
        try:
            filename = self.getFileName()
            self.compileFile()
            report = self.readVectorReport(filename)
            vectorList = self.removeDuplicateLoops(self.findLoopBlocks(report))
            self.vectors =vectorList
        except Exception as e:
            print e
            print "Unexpected Error Occured."
            response['error'] = e
            response['content'] = {}
            response['returncode'] = 0



def main():
    analyzer = VectorReportAnaLyzer()
    analyzer.addSource(arguments['fileAbsPath'])
    analyzer.execute()
    for vec in analyzer.vectors:
        print(vec.line)



if __name__ == '__main__':
    main()
