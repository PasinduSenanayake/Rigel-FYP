from FileHandler import FileHandler
from Parameter import Parameter
import re
from pprint import pprint


class Clause:

    def __init__(self, name, startIndex, source, directiveDetails):
        self.name = name
        self.details = None
        self.startIndex = startIndex
        if(directiveDetails[name]["haveParameters"]):
            self.parameters = self.findParameters(source, directiveDetails)

    def findParameters(self, source, directiveDetails):  #0-int 1-enum 2-string
        parameterStart = 0
        for index in range(self.startIndex, len(source)):
            openBracketCount = 0
            if(source[index] == "\n" or source[index] == "\\"):
                source = source[:index] + " " + source[index+1:]
            elif(source[index] == "("):
                if openBracketCount == 0:
                    parameterStart = index
                ++openBracketCount
            elif(source[index] == ")"):
                --openBracketCount
                if openBracketCount == 0:
                    parameterEnd = index
                    break
        parameterString = source[parameterStart+1:parameterEnd].replace(" ","")

        delimiters = []
        parameters = []
        parametersAndDelimiters = list(directiveDetails[self.name]["parameterPattern"])
        for char in list(parametersAndDelimiters):
            if char.isdigit():
                parameters.append(char)
            else:
                delimiters.append(char)
        delimiterRegex = '|'.join(delimiters)
        parameterList = re.split(delimiterRegex, parameterString)

        # pprint(parametersAndDelimiters)
        # pprint(delimiters)
        # pprint(parameters)
        # print self.name

        parameterObjList = []
        for i in range(len(parameters)):
            if(parameters[i] == "1"):
                # print "in"
                parameter = Parameter(parametersAndDelimiters[i], parameterList[i], directiveDetails[self.name][str(i)].split("$"))
                parameterObjList.append(parameter)
            else:
                parameter = Parameter(parameters[i], parameterList[i], None)
                parameterObjList.append(parameter)

        for i in range(len(parametersAndDelimiters)):
            if parametersAndDelimiters[i].isdigit():
                parametersAndDelimiters[i] = parameterObjList.pop(0)
        return parametersAndDelimiters
