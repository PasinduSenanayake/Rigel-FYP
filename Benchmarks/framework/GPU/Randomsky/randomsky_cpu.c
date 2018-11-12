

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>

int main(int argc, char *argv[]) {
	int ntarget;
	float x, y;

ntarget = 30000000;

	float *xa = (float *)malloc(sizeof(float)*ntarget);
	float *ya = (float *)malloc(sizeof(float)*ntarget);

	memset(xa, 0, sizeof(int)*ntarget); // initializes array to zeroes
	memset(ya, 0, sizeof(int)*ntarget);

	#pragma omp parallel for
	for (int i=0; i<ntarget; i++) {
			for (int j=0; j<100; j++) {
						y=((float)2048/(float)(RAND_MAX));
						ya[i] = asin(2.*y-1.)*180./M_PI;
						xa[i]=((float)1024/(float)(RAND_MAX)) * 360.;
		}

	}

	return(0);
}
