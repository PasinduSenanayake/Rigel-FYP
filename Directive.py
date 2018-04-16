from FileHandler import FileHandler
from Clause import Clause
import re
from pprint import pprint


class Directive:

    directivesDict = FileHandler.getInstance().readDirectives()

    def __init__(self, startIndex, sourceCode):
        self.code = sourceCode[startIndex:self.getLineEnding(sourceCode, startIndex)]
        self.name = self.findDirective()
        self.startIndex = startIndex
        self.clauses = self.findClauses()

    def findDirective(self):
        matchLen = 0
        directiveName = None
        # pprint(self.directivesDict)
        for directiveNameItr,details in self.directivesDict.items():
            regexString = directiveNameItr.replace(" "," [^\\S]*")
            # print regexString
            regex = re.compile(regexString, re.DOTALL)
            matching = regex.search(self.code)
            if(matching and matching.end()-matching.start() > matchLen):
                matchLen = matching.end()-matching.start()
                directiveName = directiveNameItr

        # pprint(self.directivesDict)
        return directiveName

    def findClauses(self): #single clause cannot be in two lines
        directive = self.code
        clauses = {}
        directiveDetails = self.directivesDict[self.name]
        for clause, details in directiveDetails["clauses"].items():
            regex = re.compile(clause, re.DOTALL)
            matching = regex.search(directive)
            if matching:
                clauses[clause] = Clause(clause,matching.start(), directive, directiveDetails["clauses"])
                directive = directive[:matching.start()] + "@"*(matching.end()-matching.start()) + directive[matching.end():]


                # print self.code[matching.start():matching.end()]
        # while (matching):
        #     loop = ForLoop(matching.start(), sourceCode)
        #     self.forLoops.append(loop)
        #     sourceCode = sourceCode[:matching.start()] + "@" * 3 + sourceCode[matching.start() + 3:]
        #     matching = regex.search(sourceCode)

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
