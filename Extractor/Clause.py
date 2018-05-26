from Block import Block
from Parameter import Parameter
import re
from pprint import pprint


class Clause(Block):

    def __init__(self, name, startIndex = 0, r_clauseStartIndex = 0, source = None, directiveDetails = None, haveParameters = False, elements = []):
        self.name = name
        self.details = directiveDetails[name]
        super(Clause, self).__init__(name, startIndex + r_clauseStartIndex)
        if(haveParameters):
            elements = self.findParameters(startIndex, r_clauseStartIndex, source, directiveDetails)
        super(Clause, self).setElements(elements)

    def findParameters(self, startIndex, r_clauseStartIndex, source, directiveDetails):  #0-int 1-enum 2-string
        parameterStart = 0
        parameterEnd = 0
        for index in range(r_clauseStartIndex, len(source)):
            openBracketCount = 0
            if(source[index] == "("):
                if openBracketCount == 0:
                    parameterStart = index
                ++openBracketCount
            elif(source[index] == ")"):
                --openBracketCount
                if openBracketCount == 0:
                    parameterEnd = index
                    break
        parameterString = source[parameterStart+1:parameterEnd]

        delimiters = None
        parameters = None
        parametersAndDelimiters = None
        parameterList = None
        clause = self.name
        offset = ""
        while(True):
            delimiters = []
            parameters = []
            parametersAndDelimiters = list(directiveDetails[self.name + offset]["parameterPattern"])
            for char in list(parametersAndDelimiters):
                if char.isdigit():
                    parameters.append(char)
                else:
                    delimiters.append(char)
            delimiterRegex = '|'.join(delimiters)
            parameterList = re.split(delimiterRegex, parameterString)

            if len(parameterList) == len(parameters):
                self.details = directiveDetails[self.name + offset]
                break
            offset = offset + "+"



        parameterObjList = []
        parameterStartIndex = startIndex + parameterStart + 1
        for i in range(len(parameters)):
            if(parameters[i] == "1"):
                parameter = Parameter(parametersAndDelimiters[i], parameterList[i], directiveDetails[self.name][str(i)].split("$"), parameterStartIndex)
                parameterObjList.append(parameter)
            else:
                parameter = Parameter(parameters[i], parameterList[i], [], parameterStartIndex)
                parameterObjList.append(parameter)
            parameterStartIndex = parameterStartIndex + len(parameterList[i]) + 1  #assuming single character delimiters

        parametersAndDelimiters.insert(0, Block("(", startIndex + parameterStart))
        parametersAndDelimiters.append(Block(")", startIndex + parameterEnd))

        for i in range(1,len(parametersAndDelimiters)-1):
            if parametersAndDelimiters[i].isdigit():
                parametersAndDelimiters[i] = parameterObjList.pop(0)
            else:
                parametersAndDelimiters[i] = Block(
                    parametersAndDelimiters[i],
                    parametersAndDelimiters[i-1].getStartIndex() + parametersAndDelimiters[i-1].length())
        return parametersAndDelimiters
