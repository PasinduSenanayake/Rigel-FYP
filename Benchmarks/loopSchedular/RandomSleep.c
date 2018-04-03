/* cc  -lm t4.c -qsmp */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>
#include <string.h>
int iterations;
int theradSize;

void dynamic_scheduling(int* randomArray){

	printf("Random Sleep...\n");

  double startTime = omp_get_wtime();
	#pragma omp parallel for num_threads(theradSize) schedule(static)
	for (int i = 0; i < iterations; i++){
		printf("Thread no = %d, i = %d\n", omp_get_thread_num(), i);
		sleep(rand() %randomArray[i]);

	}
  double endTime = omp_get_wtime();
  printf("Random Sleep End \n");
	printf("Random Sleep Time taken %f \n", (endTime  - startTime));
}


int main(int argc, char **argv){
  theradSize = strtol(argv[1], NULL, 10);
	iterations = strtol(argv[2], NULL, 10);
	char message[iterations*2];
	FILE *file_in =fopen("randnum.txt", "r");
	fscanf(file_in,"%s", message);
	char *fileData = strtok (message, ",");
	int array[iterations];
	int i = 0;
	while (fileData != NULL)
	 {
			 array[i++] = strtol(fileData, NULL, 10);
			 fileData = strtok (NULL, ",");
	 }
	 dynamic_scheduling(array);
}
