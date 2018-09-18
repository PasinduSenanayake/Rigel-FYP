import os
import sys
import argparse
from subprocess import Popen, PIPE
import re

import PermutedLoop
from Loop import Loop
from FileHandler import FileHandler
import traceback

from PermutedLoop import PermutedLoop

sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Utils")

# parser = argparse.ArgumentParser(description='Initilizer of analyzer')
# parser.add_argument('-fp', '--fpath', type=str, help='Absolute file path', required=False)
# parser.add_argument('-ca', '--carguments', type=str, help='Compiler time arguments', required=False, default="")
# parser.add_argument('-fa', '--farguments', type=str, help='Run time arguments', required=False, default="")
# args = parser.parse_args()
response = {
    "returncode":0,
    "error":"",
    "content":{}
    }
# arguments = {
#     "fileAbsPath": args.fpath,
#     "runTimeArguments": args.farguments,
#     "compTimeArguments": args.carguments
#     }

class VectorReportAnalyzer:
    def __init__(self, sources):
        self.sources = []
        self.vectors = {}
        self.addSources(sources)
        self.sourceDir = "/".join(self.sources[0].split("/")[:-1])
        self.execute()

    def addSources(self, sources):
        self.sources = sources

    def compileFile(self):
        # command = "icc -o2 -qopt-report=5 -qopt-report-phase=all '" + "' '".join(self.sources) + "'"
        sourcePaths = []

        for source in self.sources:
            tempSource = source.replace(" ", "\ ")
            sourcePaths.append(tempSource)
        command = "icc -o2 -qopt-report=5 -qopt-report-phase=all " + " ".join(sourcePaths)
        # command.replace("'", "\"")
        # print(command)
        processOutput = Popen(command, shell=True, cwd=self.sourceDir+"/_vectorization")
        stdout, stderr = processOutput.communicate()
        if(stderr==None):
            print "Compiled Successfully"
        else:
            print stderr

    def getFileName(self, source):
        fullname = source.split("/")[-1]
        # print(fullname)
        return fullname

    def readVectorReport(self,filePath):
        file = FileHandler.getInstance().readSource(filePath)
        # print("read")
        return file

    def getVectorData(self,lineNo, report ):
        line = 0
        vectorLen = 0
        speedup = 0
        overhead = 0.0
        lineregex = re.compile(r"LOOP BEGIN", re.DOTALL)
        vectorLenregex = re.compile(r"#15305")
        speedupregex = re.compile(r"#15478")
        overheadregex = re.compile(r"#15309")
        for i in range(lineNo,0,-1):
            match1 = lineregex.search(report[i])
            match2 = vectorLenregex.search(report[i])
            match4 = overheadregex.search(report[i])
            if match4:
                fullLine = report[i][:-1]
                filter(str.isalnum, fullLine)
                overhead = float(fullLine[-5:])
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
        # loop = Loop(line,vectorLen,speedup,overhead)
        loop = {"type": "vectorized_loop", "line": line,
                "vectorLen": vectorLen, "speedup": speedup,
                "overhead": overhead}
        return loop

    def getPermutedVectorData(self,lineNo, report ):
        line = 0
        vectorLen = 0
        speedup = 0
        overhead = 0.0
        permutation = {}
        lineregex = re.compile(r"LOOP BEGIN", re.DOTALL)
        vectorLenregex = re.compile(r"#15305")
        speedupregex = re.compile(r"#15478")
        overheadregex = re.compile(r"#15309")
        permutationregex = re.compile(r"#25444")
        for i in range(lineNo,0,-1):
            match1 = lineregex.search(report[i])
            match2 = vectorLenregex.search(report[i])
            match4 = overheadregex.search(report[i])
            if match4:
                fullLine = report[i][:-1]
                filter(str.isalnum, fullLine)
                overhead = float(fullLine[-5:])
            if match2:
                fullLine = report[i][:-1].strip()
                words = re.compile("\s").split(fullLine)
                # filter(str.isalnum, fullLine)
                vectorLen = int(words[6])
            if match1:
                val =report[i].split('(', 1)[1].split(')')[0]
                line = int(val.split(',')[0])
                break
        for i in range(lineNo, 0, -1):
            match5 = permutationregex.search(report[i])
            if match5:
                fullLine = report[i]
                values =re.findall('\((.*?)\)',fullLine)
                values[0] = values[0].split(' ')[1:-1]
                values[1] = values[1].split(' ')[1:-1]
                permutation = values
                break
        for i in range(lineNo,len(report),1):
            match3 = speedupregex.search(report[i])
            if match3:
                fullLine = report[i][:-1]
                speedup = fullLine.split(':')[-1].split(' ')[1]
                break
        # print(str(line)+" "+str(vectorLen)+" "+str(speedup))
        loop = {"type": "permuted_loop", "line": line,
                "vectorLen": vectorLen, "speedup": speedup,
                "overhead": overhead, "permutation": permutation}
        # loop = PermutedLoop(line, vectorLen, speedup, overhead,permutation)
        return loop

    def findLoopBlocks(self,report):
        vectorDataList= []
        for i in range(0,len(report)):
            regex1 = re.compile(r"#15300", re.DOTALL)
            match = regex1.search(report[i])
            regex2 = re.compile(r"#15301", re.DOTALL)
            match1 = regex2.search(report[i])
            if match :
                vectorData = self.getVectorData(i,report)
                if vectorData not in vectorDataList :
                    vectorDataList.append(vectorData)
            elif match1 :
                permutedData =self.getPermutedVectorData(i,report)
                if permutedData not in vectorDataList :
                    vectorDataList.append(permutedData)
        return vectorDataList

    def removeDuplicateLoops(self,loopList):
        duplicateList = []
        for vector1 in loopList:
            duplicateList.append(vector1)
            count =0
            for vector2 in duplicateList:
                if vector1["line"] == vector2["line"]:
                    count +=1
                if count >1 :
                    duplicateList.pop()
        return duplicateList

    def execute(self):
        try:
            self.compileFile()
            for source in self.sources:
                report = self.readVectorReport(self.sourceDir+"/_vectorization/"+source.split("/")[-1][0:-2]+'.optrpt')
                vectorList = self.removeDuplicateLoops(self.findLoopBlocks(report))
                self.vectors[source] = vectorList
        except Exception as e:
            print e
            traceback.print_exc()
            print "Unexpected Error Occured."
            response['error'] = e
            response['content'] = {}
            response['returncode'] = 0



# def main():
    # analyzer = VectorReportAnaLyzer()
    # analyzer.addSources(arguments['fileAbsPath'].split("|"))
    # analyzer.execute()
    # for source, vectors in analyzer.vectors.items():
    #     print len(vectors)
        # for vector in vectors:
        #     print vector
            # if vector["type"] == "permuted_loop":
            #     print(vector["line"], vector["overhead"], vector["permutation"])


# if __name__ == '__main__':
#     main()
