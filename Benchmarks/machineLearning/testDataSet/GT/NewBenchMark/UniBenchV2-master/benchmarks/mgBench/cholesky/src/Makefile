# C compiler
CC = clang


cholesky:
	$(CC) cholesky_gpu.c -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda -o runnable -lm

clean:
	rm -f *.o
