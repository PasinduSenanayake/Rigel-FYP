/*
   Erro parar gerar struct.
   Erro na anotação dos parâmetros
   This program performs K nearest neighbors on the GPU with
   dynamically allocated matrices.

    Author: Gleison Souza Diniz Mendon?a
    Date: 04-01-2015
    version 2.0

    Run:
    ipmacc k-nearest_gpu.c -o k-nearest
    ./k-nearest matrix-size
*/
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include "./mgbenchUtilFunctions.h"

#define SIZE 4096
#define SIZE_2 SIZE/2
#define GPU_DEVICE 0
#define ERROR_THRESHOLD 0.05
#define default_v 100000.00

typedef struct point
{
    int x;
    int y;
}point;

typedef struct sel_points
{
    int position;
    float value;
}sel_points;


//----> AdditionalCodeHook

void init(point *pivots, point *the_points, sel_points *selected_cpu, sel_points *selected_gpu)
{
    int i,j;
    for(i=0;i<SIZE_2;i++)
    {
        pivots[i].x = i*3;
        pivots[i].y = i*2;
    }

    for(i=0;i<SIZE;i++)
    {
        the_points[i].x = i*3;
        the_points[i].y = i*2;

        for(j=0;j<SIZE;j++)
        {
            selected_cpu[i*SIZE+j].position = 0;
            selected_cpu[i*SIZE+j].value = default_v;
            selected_gpu[i*SIZE+j].position = 0;
            selected_gpu[i*SIZE+j].value = default_v;
        }
    }
}


void k_nearest_cpu(point *pivots, point *the_points, sel_points *selected)
{
    int i,j;
    for(i=0;i<SIZE_2;i++)
    {
        for(j=0;j<SIZE;j++)
        {
            float distance,x,y;
            x = pivots[i].x - the_points[j].x;
            y = pivots[i].y - the_points[j].y;
            x = x * x;
            y = y * y;

            distance = x + y;
            distance = sqrt(distance);

            selected[i*SIZE+j].value = distance;
            selected[i*SIZE+j].position = j;
        }
    }
    
    #pragma omp parallel for
    for(i=0;i<SIZE_2;i++)
    {
        /// for each line in matrix
        /// order values
        int j;
        for(j=0;j<SIZE;j++)
        {
            int m;
            for(m=j+1;m<SIZE;m++)
            {
                if(selected[i*SIZE+j].value>selected[i*SIZE+m].value)
                {
                    sel_points aux;
                    aux = selected[i*SIZE+j];
                    selected[i*SIZE+j] = selected[i*SIZE+m];
                    selected[i*SIZE+m] = aux;
                }
            }

        }
    }
}



int main(int argc, char *argv[])
{
    double t_start, t_end;
    point *pivots;
    point *the_points;
    sel_points *selected_cpu, *selected_gpu;

    fprintf(stdout,"<< K-nearest >>\n");

    pivots = (point *) malloc(sizeof(point) * SIZE);
    the_points = (point *) malloc(sizeof(point) * SIZE);
    selected_cpu = (sel_points *)malloc(sizeof(sel_points) * SIZE * SIZE);
    selected_gpu = (sel_points *)malloc(sizeof(sel_points) * SIZE * SIZE);

    init(pivots, the_points, selected_cpu, selected_gpu);


    t_start = rtclock();
    k_nearest_cpu(pivots, the_points, selected_cpu);
    t_end = rtclock();
    fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_end - t_start);


    free(selected_cpu);
    free(selected_gpu);
    free(pivots);
    free(the_points);

    return 0;
}
