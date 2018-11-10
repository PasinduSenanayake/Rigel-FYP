# C compiler
CC = clang -fopenmp


prime_counter:
	$(CC) prime_counter_Static.c -o runnableStatic
	$(CC) prime_counter_Guided.c -o runnableGuided
	$(CC) prime_counter_Dynamic.c -o runnableDynamic

clean:
	rm -f *.o
