
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include "./mgbenchUtilFunctions.h"

#define SIZE 12000
#define GPU_DEVICE 0
#define PERCENT_DIFF_ERROR_THRESHOLD 0.01


void init(float *a)
{
	int i;
	for (i = 0; i < SIZE; ++i)
	{
        	a[i] = 2*i+7;
	}
}

int search_GPU(float *a, float c)
{
    int i;
    int find = -1;

     for (int j = 0; j < SIZE; ++j)
     {
        for (i = 0; i < SIZE; ++i)
        {
	         if(a[i] == c)
	          {
	             find = i;
	              i=SIZE;
	             }
        }

    }

    return find;
}

int main(int argc, char *argv[]) {
    double t_start, t_end;
    float *a, c;
    int find_cpu, find_gpu;

    a = (float *) malloc(sizeof(float) * SIZE);
    c = (float) SIZE-5;

    init(a);

    t_start = rtclock();
    find_gpu = search_GPU(a, c);
    t_end = rtclock();


    free(a);

    return 0;
}
