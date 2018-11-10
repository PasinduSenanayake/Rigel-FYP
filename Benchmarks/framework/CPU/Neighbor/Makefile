# C compiler
CC = clang -fopenmp


fdtd2d:
	$(CC) neighbor_bench_Static.c -o runnableStatic -lm
	$(CC) neighbor_bench_Dynamic.c -o runnableDynamic -lm
	$(CC) neighbor_bench_Guided.c -o runnableGuided -lm

clean:
	rm -f *.o
