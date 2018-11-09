# C compiler
CC = clang -fopenmp


pi:
	$(CC) pi_cpu_Static.c -o runnableStatic
	$(CC) pi_cpu_Dynamic.c -o runnableDynamic
	$(CC) pi_cpu_Guided.c -o runnableGuided

clean:
	rm -f *.o
