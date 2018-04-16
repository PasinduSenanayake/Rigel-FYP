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
            self.findParameters(source, directiveDetails)

    def findParameters(self, source, directiveDetails):  #0-int 1-enum 2-string
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
        for char in list(directiveDetails[self.name]["parameterPattern"]):
            if char.isdigit():
                parameters.append(char)
            else:
                delimiters.append(char)
        delimiterRegex = '|'.join(delimiters)
        parameterList = re.split(delimiterRegex, parameterString)
        for i in range(len(parameters)):
            if(parameters[i] == 1):
                parameter = Parameter(parameters[i], parameterList[i], directiveDetails[self.name][str(i)].split("$"))
            else:
                parameter = Parameter(parameters[i], parameterList[i])
                # how to store parameters


