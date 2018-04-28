from FileHandler import FileHandler
from Clause import Clause
from Block import Block
from Parameter import Parameter
import re
from pprint import pprint


class Directive(Block):

    directivesDict = FileHandler.getInstance().readDirectives()

    def __init__(self, startIndex, sourceCode):
        directiveString = sourceCode[startIndex:self.getLineEnding(sourceCode, startIndex)]
        foundDirective = self.findDirective(directiveString)
        self.name = foundDirective[0]
        sourceDirective = foundDirective[1]
        self.details = self.directivesDict[self.name]
        elements = self.findClauses(startIndex, directiveString)
        super(Directive, self).__init__(startIndex, sourceDirective)
        super(Directive, self).setElements(elements)

    def findDirective(self, directiveString):
        matchLen = 0
        directiveName = None
        # pprint(self.directivesDict)
        for directiveNameItr,details in self.directivesDict.items():
            regexString = directiveNameItr.replace(" "," [^\\S]*")
            regex = re.compile(r"#[^\S]*pragma[^\S]*omp[^\S]*" + regexString, re.DOTALL)
            matching = regex.search(directiveString)
            if(matching and matching.end()-matching.start() > matchLen):
                matchLen = matching.end()-matching.start()
                directiveName = directiveNameItr
        return [directiveName, directiveString[:matchLen+1]]

    def findClauses(self, startIndex, directiveString): #single clause cannot be in two lines
        directive = directiveString
        clauses = []
        directiveDetails = self.directivesDict[self.name]
        for clause, details in directiveDetails["clauses"].items():
            regex = None
            if(details["haveParameters"]):
                regex = re.compile(clause+"[^\\S]*\(", re.DOTALL)
            else:
                regex = re.compile(clause, re.DOTALL)
            matching = regex.search(directive)
            if matching:
                clauses.append(Clause(clause, startIndex, matching.start(), directive, directiveDetails["clauses"]))
                directive = directive[:matching.start()] + "@"*(matching.end()-matching.start()) + directive[matching.end():]
        return clauses

    def getLineEnding(self, string, startIndex):
        lineBreaks = 0
        directiveLength = 0
        for char in string[startIndex:]:
            directiveLength += 1
            if char == "\\":
                lineBreaks = lineBreaks + 1
            elif char == "\n":
                if lineBreaks == 0:
                    break
                lineBreaks = lineBreaks - 1
        return startIndex+directiveLength

    def setSchedule(self, mechanism):
        for clause in self.elements:
            # print clause.name
            if clause.name == "schedule":
                for parameter in clause.elements:
                    if isinstance(parameter, Parameter):
                        if len(parameter.enums) > 0 and mechanism in parameter.enums:
                            parameter.body = mechanism

    def setScheduleByLine(self, lineNumber, mechanism):
        if self.lineNumber == lineNumber:
            for clause in self.elements:
                # print clause.name
                if clause.name == "schedule":
                    for parameter in clause.elements:
                        if isinstance(parameter, Parameter):
                            if len(parameter.enums) > 0 and mechanism in parameter.enums:
                                parameter.body = mechanism
