from pprint import pprint
from Block import Block


class Parameter(Block):

    def __init__(self, type, value, enums , startIndex):
        self.type = type
        self.enums = enums
        super(Parameter, self).__init__(startIndex, value)
