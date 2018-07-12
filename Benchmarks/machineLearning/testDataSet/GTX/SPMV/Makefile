# C compiler
CC = clang


spvm:parboil.o mmio.o convert_dataset.o
	$(CC) spmv_profile.c parboil.o mmio.o convert_dataset.o -o runnable -lm

parboil.o: parboil.c parboil.h
		$(CC)  parboil.c -c

convert_dataset.o:convert_dataset.c convert_dataset.h
	$(CC)  convert_dataset.c -c

mmio.o: mmio.c mmio.h
		$(CC)  mmio.c -c


clean:
	rm -f *.o
