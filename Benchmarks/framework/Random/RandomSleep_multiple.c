#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>
#include <string.h>
int iterations;
int theradSize;


//----> AdditionalCodeHook


void dynamic_scheduling(int* randomArray){

	printf("Random Sleep...\n");

	#pragma omp parallel for num_threads(theradSize) schedule(static)
	for (int i = 0; i < 10; i++){
		printf("Thread no = 1 i =1 \n");
		sleep(i*2);
		}
	#pragma omp parallel for num_threads(theradSize) schedule(static)
	for (int i = 0; i < 10; i++){
		printf("Thread no = 1 i =1 \n");
		sleep(i*2);
		}

}



int main(int argc, char **argv){
  theradSize = 4;
	iterations = strtol(argv[1], NULL, 10);
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
