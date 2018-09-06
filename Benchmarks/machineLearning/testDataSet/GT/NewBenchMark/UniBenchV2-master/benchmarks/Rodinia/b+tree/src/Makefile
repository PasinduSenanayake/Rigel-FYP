# C compiler
CC = clang


btree:kernel_cpu.o kernel_cpu_2.o timer.o num.o
	$(CC) kernel_cpu.o kernel_cpu_2.o timer.o num.o main.c -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda -o runnable -lm

kernel_cpu.o:kernel_cpu.c kernel_cpu.h
	$(CC) kernel_cpu.c -c -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda

kernel_gpu.o:kernel_cpu_2.c kernel_cpu_2.h
	$(CC) kernel_cpu_2.c -c -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda

timer.o:timer.h timer.c
	$(CC) timer.c -c -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda

num.o:num.c num.h
	$(CC) num.c -c -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda
clean:
	rm -f *.o

#run ./runnable -i path
#eg ./runnable -i /home/piyumi/FYP/code_fragments/samples/Unibench/benchmarks/Parboil/mri-q/src/MRI-Q/64_64_64_dataset.bin 
