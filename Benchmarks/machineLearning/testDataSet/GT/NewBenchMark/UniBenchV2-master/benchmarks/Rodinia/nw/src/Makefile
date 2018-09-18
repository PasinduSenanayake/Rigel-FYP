# C compiler
CC = clang


needle:
	$(CC) -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda needle.c -o runnable -lm



clean:
	rm -f *.o

#run ./runnable -i path
#eg ./runnable -i /home/piyumi/FYP/code_fragments/samples/Unibench/benchmarks/Parboil/mri-q/src/MRI-Q/64_64_64_dataset.bin 
