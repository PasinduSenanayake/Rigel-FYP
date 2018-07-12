from Extractor import Extractor
from Parameter import Parameter
from Directive import Directive
from StructuredBlock import StructuredBlock
from ForLoop import ForLoop
import logging, sys


def setSchedule(sourceObj, mechanism, lineNumber = None):
    nextObj = sourceObj.root
    while nextObj:
        if isinstance(nextObj, Directive):
            if lineNumber:
                if nextObj.lineNumber == lineNumber:
                    for clause in nextObj.elements:
                        # print clause.name
                        if clause.name == "schedule":
                            for parameter in clause.elements:
                                if isinstance(parameter, Parameter):
                                    if len(parameter.enums) > 0 and mechanism in parameter.enums:
                                        parameter.body = mechanism
            else:
                for clause in nextObj.elements:
                    # print clause.name
                    if clause.name == "schedule":
                        for parameter in clause.elements:
                            if isinstance(parameter, Parameter):
                                if len(parameter.enums) > 0 and mechanism in parameter.enums:
                                    parameter.body = mechanism
        nextObj = nextObj.getNext()

# extractor = Extractor()
# sourceObj = extractor.addSource("omp_hello.c")
# setSchedule(sourceObj, "static")
# # setSchedule(sourceObj, "static", 21)
# # temp = sourceObj.root
# # temp.body = "wow"
# sourceObj.writeToFile("out.c")
#
# nextObj = sourceObj.root
# while nextObj:
#     if isinstance(nextObj, ForLoop):
#         if nextObj.hasPragma():
#             print nextObj.lineNumber
#     nextObj = nextObj.getNext()

# print sourceObj.root.getNext().isChild(sourceObj.root.parent)

# print sourceObj.root.getContent()

extractor = Extractor()
sourceObj = extractor.addSource("omp_hello.c")

sourceObj.writeToFile("serial.c", sourceObj.serialroot)
sourceObj.writeToFile("parallel.c", sourceObj.root)
print(sourceObj.serialparalleMapping)
