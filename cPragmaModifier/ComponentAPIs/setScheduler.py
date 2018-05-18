import logging, sys
from ..Parameter import Parameter
from ..Directive import Directive

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
