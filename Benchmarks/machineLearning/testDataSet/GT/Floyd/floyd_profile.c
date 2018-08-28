

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include "./mgbenchUtilFunctions.h"

#define SIZE 400
#define GPU_DEVICE 0
#define ERROR_THRESHOLD 0.05

/// initialize the cartesian map
void init(int *matrix, int *matrix_dist_cpu, int *matrix_dist_gpu)
{
    int i,j,r,m;
    for(i=0;i<SIZE;i++)
    {
        for(j=0;j<SIZE;j++)
        {
            matrix[i*SIZE+j] = 99999999;
            matrix_dist_cpu[i*SIZE+j] = 99999999;
	    matrix_dist_gpu[i*SIZE+j] = 99999999;
        }
    }

    for(i=0;i<SIZE;i++)
    {
        r = (i*97)%SIZE;
        for(j=0;j<r;j++)
        {
            m = (((j*1021)*71 % (SIZE * SIZE))+1);
            matrix[i*SIZE+j] = m;
            if(i==j){matrix[i*SIZE+j] = 0; }
        }
    }
}


/// Knearest algorithm GPU
/// s = size of cartesian map
void Knearest_GPU(int *matrix, int *matrix_dist)
{
    int i,j,k;
    for(i=0;i<SIZE;i++)
    {
        for(j=0;j<SIZE;j++)
        {
            if(matrix[i*SIZE+j]!=99999999)
            {
                matrix_dist[i*SIZE+j] = matrix[i*SIZE+j];
            }
        }
        matrix_dist[i*SIZE+i] = 0;
    }

    /// opportunity of parallelism here
        for(i=0;i<SIZE;i++)
        {

            for(k=0;k<SIZE;k++)
            {
                for(j=0;j<SIZE;j++)
                {
                    if(matrix_dist[k*SIZE+i]!=99999999 && matrix_dist[i*SIZE+j]!=99999999 &&
                       matrix_dist[k*SIZE+j]>matrix_dist[k*SIZE+i]+matrix_dist[i*SIZE+j])
                    {
                         matrix_dist[k*SIZE+j] = matrix_dist[k*SIZE+i] + matrix_dist[i*SIZE+j];
                    }
                }
            }
        }

}



int main(int argc, char *argv[])
{
    int i;
    int points, var;
    double t_start, t_end;

    int *matrix;
    int *matrix_dist_cpu, *matrix_dist_gpu;

    matrix = (int*) malloc(sizeof(int) * SIZE * SIZE);
    matrix_dist_gpu = (int*) malloc(sizeof(int) * SIZE * SIZE);

    init(matrix, matrix_dist_cpu, matrix_dist_gpu);

    t_start = rtclock();
    Knearest_GPU(matrix, matrix_dist_gpu);
    t_end = rtclock();

    free(matrix_dist_gpu);

    return 0;
}
