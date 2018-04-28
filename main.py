from Extractor import Extractor
import logging, sys


extractor = Extractor()
sourceObj = extractor.addSource("omp_hello.c")
sourceObj.setSchedule("static")
sourceObj.setScheduleByLine(21,"static")
sourceObj.writeToFile("out.c")



