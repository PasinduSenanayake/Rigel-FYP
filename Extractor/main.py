from Extractor import Extractor
from Parameter import Parameter
from Directive import Directive
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

extractor = Extractor()
sourceObj = extractor.addSource("omp_hello.c")
setSchedule(sourceObj, "static")
# setSchedule(sourceObj, "static", 21)
# temp = sourceObj.root
# temp.body = "wow"
sourceObj.writeToFile("out.c")

# print sourceObj.root.getNext().isChild(sourceObj.root.parent)

# print sourceObj.root.getContent()






