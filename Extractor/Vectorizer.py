
class Vectorizer:
    def vectorize(self, forLoop, instructionSet, dataTypeSize):
        if forLoop.hasPragma():
            print "this loop has pragma"