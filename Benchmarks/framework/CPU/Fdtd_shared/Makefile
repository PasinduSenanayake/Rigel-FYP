# C compiler
CC = clang -fopenmp


fdtd2d:
	$(CC) Fdtd2_workshare_Static.c -o runnableStatic -lm
	$(CC) Fdtd2_workshare_Dynamic.c -o runnableDynamic -lm
	$(CC) Fdtd2_workshare_Guided.c -o runnableGuided -lm

clean:
	rm -f *.o
