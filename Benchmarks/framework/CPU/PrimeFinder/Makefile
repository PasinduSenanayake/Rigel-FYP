# C compiler
CC = clang -fopenmp


cpuBench:
	$(CC) CpuBenchPrimeFinder_Static.c -o runnableStatic -lgmp  -lssl -lcrypto
	$(CC) CpuBenchPrimeFinder_Guided.c -o runnableGuided -lgmp  -lssl -lcrypto
	$(CC) CpuBenchPrimeFinder_Dynamic.c -o runnableDynamic -lgmp  -lssl -lcrypto

clean:
	rm -f *.o
