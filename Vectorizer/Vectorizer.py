from VectorReportAnalyzer import VectorReportAnalyzer


class Vectorizer():
    def __init__(self, extractor):
        # self.analyzer = VectorReportAnalyzer(["/home/praveen/FYP/Benchmarks/Vectorization Benchmark/TSVC/tsc.c",
        #                         "/home/praveen/FYP/Benchmarks/Vectorization Benchmark/TSVC/dummy.c"])
        sourcePaths = extractor.getSourcePathList()
        self.analyzer = VectorReportAnalyzer(sourcePaths)
        for filePath, vectorList in analyzer.vectors.items():
            source = extractor.getSource(filePath)
            for vector in vectorList:
                if vector["type"] == "vectorized_loop":
                    source.vectorize(vector["line"], vector["vectorLen"])


