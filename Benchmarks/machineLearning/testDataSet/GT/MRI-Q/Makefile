# C compiler
CC = clang


mriqCPU:parboil.o
	$(CC) mri-q_profile.c parboil.o -o runnable -lm

parboil.o: parboil.c parboil.h
		$(CC)  parboil.c -c

clean:
	rm -f *.o

#run ./runnable -i path
#eg ./runnable -i /home/piyumi/FYP/code_fragments/samples/Unibench/benchmarks/Parboil/mri-q/src/MRI-Q/64_64_64_dataset.bin 
