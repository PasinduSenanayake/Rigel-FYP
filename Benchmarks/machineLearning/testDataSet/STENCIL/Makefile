# C compiler
CC = clang


stencil:parboil.o
	$(CC) stencil_profile.c parboil.o -o runnable -lm

parboil.o: parboil.c parboil.h
		$(CC)  parboil.c -c

clean:
	rm -f *.o
