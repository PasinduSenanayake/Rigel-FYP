import re

class Block(object):
    def __init__(self, startIndex, body):
        self.startIndex = startIndex
        self.body = body
        self.innerSpacing = ""
        self.outerSpacing = ""
        self.elements = []

    def setElements(self, elements):
        elements.sort(key=lambda x: x.getStartIndex(), reverse=False)
        self.elements = elements

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
                    element.outerSpacing = source[element.getEndIndex()+1:self.elements[n+1].getStartIndex()]


    def getContent(self):
        string = self.body + self.innerSpacing
        for element in self.elements:
            string = string + element.getContent()
        string = string + self.outerSpacing
        return string

    def length(self):
        length = len(self.body + self.innerSpacing + self.outerSpacing)
        for element in self.elements:
            length = length + element.length()
        return length

    def getStartIndex(self):
        return self.startIndex

    def getEndIndex(self):
        return self.startIndex + self.length() - 1

    def isChild(self, parent):
        if parent.getStartIndex() < self.getStartIndex() and self.getStartIndex() < parent.getEndIndex():
            return True
        return False


