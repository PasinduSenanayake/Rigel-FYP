import re
from ForLoop import ForLoop
from Directive import Directive
from pprint import pprint

class SourceCode:
    def __init__(self, code):
        self.code = code
        self.forLoops = []
        self.directives = []
        self.structure = []
        self.removeBlockComments()
        self.removeLineComments()
        self.searchForLoops()
        self.searchDirectives()

    def removeBlockComments(self):
        regex = re.compile(r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)",
                           re.DOTALL)  # error if block comment syntax found in a string construct or in a line comment
        matching = regex.search(self.code)
        while (matching):
            self.code = self.code[:matching.start()] + self.code[matching.end():]
            matching = regex.search(self.code)

    def removeLineComments(self):
        regex = re.compile(r"(//.*)", re.DOTALL)  # error if line comment syntax found in a string construct or in a block comment
        matching = regex.search(self.code)
        while (matching):
            commentLength = 0
            for char in self.code[matching.start():]:
                commentLength += 1
                if char == "\n":
                    break
            self.code = self.code[:matching.start()] + self.code[matching.start() + commentLength - 1:]
            matching = regex.search(self.code)

    def searchForLoops(self):
        sourceCode = self.code
        regex = re.compile(r"for[^\S]*\(", re.DOTALL)  # playfor() method will be caught too
        matching = regex.search(sourceCode)
        while (matching):
            loop = ForLoop(matching.start(),sourceCode)
            self.forLoops.append(loop)
            sourceCode = sourceCode[:matching.start()] + "@" * 3 + sourceCode[matching.start() + 3:]
            matching = regex.search(sourceCode)

    def searchDirectives(self):      # assumed "\" is not within pragma directive
        sourceCode = self.code
        regex = re.compile(r"#[^\S]*pragma[^\S]*omp", re.DOTALL)
        matching = regex.search(sourceCode)
        while (matching):
            directive = Directive(matching.start(),sourceCode)
            self.directives.append(directive)
            sourceCode = sourceCode[:matching.start()] + "@@@" + sourceCode[matching.start() + 3:]
            matching = regex.search(sourceCode)




