from FileHandler import FileHandler
from Clause import Clause
from Block import Block
from Parameter import Parameter
import re
from pprint import pprint


class Directive(Block):

    directivesDict = FileHandler.getInstance().readDirectives()

    def __init__(self, startIndex, sourceCode = None, name = None , elements = None):
        if name:
            self.name = name
            super(Directive, self).__init__("#pragma omp " + name, startIndex)
        else:
            directiveString = sourceCode[startIndex:self.getLineEnding(sourceCode, startIndex)]
            foundDirective = self.findDirective(directiveString)
            self.name = foundDirective[0]
            sourceDirective = foundDirective[1]
            self.details = self.directivesDict[self.name]
            super(Directive, self).__init__(sourceDirective, startIndex)
            if not elements:
                elements = self.findClauses(startIndex, directiveString)
        if elements:
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
        return [directiveName, directiveString[:matchLen]]  #was [:matchLen+1]

    def findClauses(self, startIndex, directiveString): #single clause cannot be in two lines
        directive = directiveString
        clauses = []
        directiveDetails = self.directivesDict[self.name]
        possibleClauses = directiveDetails["general"]["clauses"].split(",")
        for clause in possibleClauses:
            # regex = None
            # if(directiveDetails["clauses"][clause]["haveParameters"]):
            regex = re.compile(clause+"[^\\S]*\(", re.DOTALL)
            # else:
            #     regex = re.compile(clause, re.DOTALL)
            matching = regex.search(directive)
            if matching:
                clauses.append(Clause(clause, startIndex, matching.start(), directive, directiveDetails["clauses"], haveParameters = True))
                directive = directive[:matching.start()] + "@"*(matching.end()-matching.start()) + directive[matching.end():]
            else:
                for clauseID, details in directiveDetails["clauses"].items():
                    if clause in clauseID and not details["haveParameters"]:
                        regex = re.compile(clause, re.DOTALL)
                        matching = regex.search(directive)
                        if matching:
                            # print directive[matching.start():matching.end()]
                            clauses.append(Clause(clause, startIndex, matching.start(), directive, directiveDetails["clauses"], haveParameters = False))
                            directive = directive[:matching.start()] + "@"*(matching.end()-matching.start()) + directive[matching.end():]
                        break
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

    def modifyClause(self, clauseName, content):
        for clause in self.elements:
            if clause.body == clauseName:
                clause.elements = []
                parameter = Parameter(0, str(content), [])
                parameter.parent = clause
                clause.elements.append(parameter)

    def hasClause(self, clause):
        fullDirective = self.getContent()
        if clause in fullDirective:
            return True
        else:
            return False

    def addClause(self, clause, content):
        fullDirective = self.getContent()
        clauseBlock = Block(" " + clause + "(" + content + ")")
        clauseBlock.parent = self
        if clause not in fullDirective:
            self.elements.insert(0, clauseBlock)
        else:
            for i in range(len(self.elements)):
                if clause in self.elements[i].body:
                    del self.elements[i]
                    break
            self.elements.insert(0, clauseBlock)




    # def setSchedule(self, mechanism):
    #     for clause in self.elements:
    #         # print clause.name
    #         if clause.name == "schedule":
    #             for parameter in clause.elements:
    #                 if isinstance(parameter, Parameter):
    #                     if len(parameter.enums) > 0 and mechanism in parameter.enums:
    #                         parameter.body = mechanism
