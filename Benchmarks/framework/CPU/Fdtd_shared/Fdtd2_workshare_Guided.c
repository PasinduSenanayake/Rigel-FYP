/* cc  -lm t4.c -qsmp */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>
#include <sys/time.h>
#include <math.h>
#include <unistd.h>
#include <string.h>


float arrayAdd(int i){

	int j =0;
	int k =0;
	int l =0;
	float tmp = 0.0;
	for (j=0; j<i;j++){
		for (k=0; k<i;k++){
			for (l=0; l<i;l++){
				if (tmp == 0.0){

					 tmp = exp((float)j) * exp((float)k) / exp((float)l);
				}
				else{
					tmp = tmp + exp((float)(j+1)) * exp((float)(k+1)) / exp((float)l);
				}
			}
		}
	}
	return tmp;

}

void dynamic_scheduling(){

double startTime = omp_get_wtime();
	#pragma omp parallel for schedule(guided)
	for (int i = 0; i < 10; i++){
		arrayAdd(i*50);
	}

  printf("Runtime Guided CoreTest: %f\n",omp_get_wtime()-startTime );
}


int main(int argc, char **argv){

	 dynamic_scheduling();
}
