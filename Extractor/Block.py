import re
# from Directive import Directive

class Block(object):
    def __init__(self, body, startIndex = 0):
        self.startIndex = startIndex
        self.body = body
        self.innerSpacing = ""
        self.outerSpacing = ""
        self.elements = []
        self.lineNumber = 0
        self.parent = None

    def setElements(self, elements):
        elements.sort(key=lambda x: x.getStartIndex(), reverse=False)
        for element in elements:
            element.parent = self
        self.elements = elements

    def addElement(self, index, element):
        element.parent = self
        self.elements.insert(index, element)

    def haveElements(self):
        if(len(self.elements) > 0):
            return True
        return False

    def fillSpaces(self, source):
        if self.haveElements():
            self.innerSpacing = source[self.startIndex+len(self.body):self.elements[0].getStartIndex()]
            for n, element in enumerate(self.elements):
                element.fillSpaces(source)
                if not n == len(self.elements) - 1:
                    spacing = source[element.getEndIndex()+1:self.elements[n+1].getStartIndex()]
                    element.outerSpacing = spacing
                    # if "\n" in spacing:
                    #     breakIndex = spacing.index("\n")
                    #     element.outerSpacing = spacing[:breakIndex + 1]
                    #     self.elements[n + 1].preSpacing = spacing[breakIndex+1:]
                    # else:
                    #     element.outerSpacing = spacing

    def length(self):
        length = len(self.body + self.innerSpacing + self.outerSpacing)
        for element in self.elements:
            length = length + element.length()
        return length

    def getStartIndex(self):
        return self.startIndex

    def getEndIndex(self):
        return self.startIndex + self.length() - 1

    def isChildByIndex(self, parent):
        if parent.getStartIndex() < self.getStartIndex() and self.getStartIndex() < parent.getEndIndex():
            return True
        return False

    def isChild(self, parent):
        if parent == None:
            return True
        if self in parent.elements:
            return True
        for element in parent.elements:
            if self.isChild(element):
                return True
        return False


    # def setSchedule(self, lineNumber, mechanism):
    #     for element in self.elements:
    #         element.setSchedule(lineNumber, mechanism)

    def setLineNumber(self, currentLine):
        self.lineNumber = currentLine
        if "\n" in self.body:
            currentLine = currentLine + self.body.count("\n")
        if "\n" in self.innerSpacing:
            currentLine = currentLine + self.innerSpacing.count("\n")
        for element in self.elements:
            currentLine = element.setLineNumber(currentLine)
        if "\n" in self.outerSpacing:
            currentLine = currentLine + self.outerSpacing.count("\n")
        return currentLine

    def getNext(self, childIndex = 0):
        if len(self.elements) > childIndex:
            return self.elements[childIndex]
        elif self.parent:
            childIndex = self.parent.elements.index(self)
            return self.parent.getNext(childIndex+1)
        return None

    # def getNextChild(self, childIndex = 0, parent = None):
    #     if len(self.elements) > childIndex:
    #         return self.elements[childIndex]
    #     elif self.parent:
    #         childIndex = self.parent.elements.index(self)
    #         if parent:
    #             if self.isChild(parent):
    #                 return self.parent.getNextChild(childIndex+1, parent)
    #         else:
    #             return self.parent.getNextChild(childIndex + 1, self)
    #     return None

    def getParent(self):
        return self.parent

    def getContent(self):
        string = self.body + self.innerSpacing
        # if self.parent:
        #     string = string + self.parent.body + " - parent\n"
        for element in self.elements:
            string = string + element.getContent()
        string = string + self.outerSpacing
        return string

    # def getNestedLoops(self, loopLines, currentLevel):
    #     for element in self.elements:
    #         loopLines = loopLines + element.getNestedLoops(loopLines,currentLevel)
    #     return loopLines


