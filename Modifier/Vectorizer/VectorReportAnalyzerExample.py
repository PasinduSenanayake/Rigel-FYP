from VectorReportAnalyzer import VectorReportAnaLyzer


def main():
    analyzer = VectorReportAnaLyzer()
    analyzer.addSource('/home/thulana/FYP/Rigel-FYP/simd.c')
    analyzer.execute()
    for vec in analyzer.vectors:
        print(vec.line)



if __name__ == '__main__':
    main()