

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include "./mgbenchUtilFunctions.h"

#define SIZE 3200
#define GPU_DEVICE 0
#define ERROR_THRESHOLD 0.05

//----> AdditionalCodeHook


void init(int *matrix, int *matrix_dist_gpu)
{
    int i,j,r,m;
    for(i=0;i<SIZE;i++)
    {
        for(j=0;j<SIZE;j++)
        {
            matrix[i*SIZE+j] = 99999999;
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


void Knearest_GPU(int *matrix, int *matrix_dist)
{
    double t_start, t_end;

    for(int i=0;i<SIZE;i++)
    {
        for(int j=0;j<SIZE;j++)
        {
            if(matrix[i*SIZE+j]!=99999999)
            {
                matrix_dist[i*SIZE+j] = matrix[i*SIZE+j];
            }
        }
        matrix_dist[i*SIZE+i] = 0;
    }

    t_start = rtclock();
    #pragma omp target map(tofrom: matrix_dist[:SIZE*SIZE])
      #pragma omp teams
      #pragma omp distribute parallel for collapse(2)
        for(int i=0;i<SIZE;i++)
        {
            for(int k=0;k<SIZE;k++)
            {
                for(int j=0;j<SIZE;j++)
                {
                    if(matrix_dist[k*SIZE+i]!=99999999 && matrix_dist[i*SIZE+j]!=99999999 &&
                       matrix_dist[k*SIZE+j]>matrix_dist[k*SIZE+i]+matrix_dist[i*SIZE+j])
                    {
                         matrix_dist[k*SIZE+j] = matrix_dist[k*SIZE+i] + matrix_dist[i*SIZE+j];
                    }
                }
            }
        }
        t_end = rtclock();

        printf("%lf\n",t_end - t_start );

}



int main(int argc, char *argv[])
{
    int i;
    int points, var;


    int *matrix;
    int *matrix_dist_gpu;

    matrix = (int*) malloc(sizeof(int) * SIZE * SIZE);
    matrix_dist_gpu = (int*) malloc(sizeof(int) * SIZE * SIZE);

    init(matrix, matrix_dist_gpu);


    Knearest_GPU(matrix, matrix_dist_gpu);


    free(matrix_dist_gpu);

    return 0;
}
