
from Tuner import Tuner

import logging, sys
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# logging.debug('A debug message!')
# logging.info('We processed %d records', len(processed_records))

tuner = Tuner()
tuner.addSource("omp_hello.c")

# sourceCodeObj = SourceCode(fileHandler.readSource())
#
#
#
#
# sourceCodeObj.searchForLoops()
# print sourceCodeObj.code
# sourceCodeObj.searchDirectives()
# for i in sourceCodeObj.forLoops:
#     print i.loopBody
# sourceCodeObj.searchDirectives()



