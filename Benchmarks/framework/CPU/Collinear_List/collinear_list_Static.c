
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <omp.h>
#include <limits.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include "./mgbenchUtilFunctions.h"

int SIZE = 1024;
#define GPU_DEVICE 0
#define PERCENT_DIFF_ERROR_THRESHOLD 0.05

typedef struct point
{
	int x;
	int y;
} point;

point *points;

void generate_points()
{
	int i;
	for(i=0;i<SIZE;i++)
	{
		points[i].x = (i*777)%11;
		points[i].y = (i*777)%13;
	}
}

//----> AdditionalCodeHook


int colinear_list_points_GPU()
{
	int i,j,k,p,val;
	val = 0;
	p = 10000;

	int *parallel_lines;
	parallel_lines = (int *) malloc(sizeof(int)*p);
	for(i=0;i<p;i++)
	{
		parallel_lines[i] = 0;
	}


	#pragma omp parallel for schedule(static)
	for(int i = 0; i < SIZE; i++)
	{
		for(int j = 0; j < SIZE; j++)
		{
			for(int k = 0; k < SIZE; k++)
			{
				/// to understand if is colinear points
				int slope_coefficient,linear_coefficient;
				int ret;
				ret = 0;
				slope_coefficient = points[j].y - points[i].y;
				if((points[j].x - points[i].x)!=0)
				{
					slope_coefficient = slope_coefficient / (points[j].x - points[i].x);
					linear_coefficient = points[i].y - (points[i].x * slope_coefficient);
					if(slope_coefficient!=0 &&linear_coefficient!=0
						&&points[k].y == (points[k].x * slope_coefficient) + linear_coefficient)
						{
							ret = 1;
						}
					}
					if(ret==1)
					{
						parallel_lines[(i%p)] = 1;
					}
				}
			}
		}



		val = 0;
		for(i=0;i<p;i++)
		{
			if(parallel_lines[i]==1)
			{
				val = 1;
				break;
			}
		}

		free(parallel_lines);

		return val;
	}



	int main(int argc, char *argv[])
	{
		double t_start, t_end;
		int result_CPU, result_GPU;

		points = (point *) malloc(sizeof(points)*SIZE);
		generate_points();

		t_start = rtclock();
		result_GPU = colinear_list_points_GPU();
		t_end = rtclock();
		fprintf(stdout, "Runtime Static CoreTest: %0.6lfs\n", t_end - t_start);
		free(points);

		return 0;
	}
