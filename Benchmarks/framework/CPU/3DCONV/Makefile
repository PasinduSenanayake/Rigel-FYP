# C compiler
CC = clang


3DConvolution:
	$(CC) 3DConvolution_Static.c -o runnableStatic
	$(CC) 3DConvolution_Static.c -o runnableDynamic
	$(CC) 3DConvolution_Guided.c -o runnableGuided

clean:
	rm -f *.o
