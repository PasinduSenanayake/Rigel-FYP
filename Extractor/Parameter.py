from pprint import pprint
from Block import Block


class Parameter(Block):

    def __init__(self, type, value, enums , startIndex = 0):
        self.type = type
        self.enums = enums
        super(Parameter, self).__init__(value, startIndex)
