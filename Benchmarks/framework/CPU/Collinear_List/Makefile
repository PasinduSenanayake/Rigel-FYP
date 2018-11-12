# C compiler
CC = clang


collinear_list_profile:
	$(CC) collinear_list_Static.c -o runnableStatic
	$(CC) collinear_list_Dynamic.c -o runnableDynamic
	$(CC) collinear_list_Guided.c -o runnableGuided

clean:
	rm -f *.o
