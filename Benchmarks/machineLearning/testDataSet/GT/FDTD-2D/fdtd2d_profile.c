

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include <omp.h>

#include "./polybenchUtilFuncts.h"


#define PERCENT_DIFF_ERROR_THRESHOLD 10.05

#define GPU_DEVICE 1

/* Problem size */
#define tmax 65536*8
#define NX 32
#define NY 32

typedef float DATA_TYPE;

void init_arrays(DATA_TYPE* _fict_, DATA_TYPE* ex, DATA_TYPE* ey, DATA_TYPE* hz)
{
  int i, j;

  for (i = 0; i < tmax; i++)
    {
      _fict_[i] = (DATA_TYPE) i;
    }

  for (i = 0; i < NX; i++)
    {
      for (j = 0; j < NY; j++)
	{
	  ex[i*NY + j] = ((DATA_TYPE) i*(j+1) + 1) / NX;
	  ey[i*NY + j] = ((DATA_TYPE) (i-1)*(j+2) + 2) / NX;
	  hz[i*NY + j] = ((DATA_TYPE) (i-9)*(j+4) + 3) / NX;
	}
    }
}

void init_array_hz(DATA_TYPE* hz)
{
  int i, j;

  for (i = 0; i < NX; i++)
    {
      for (j = 0; j < NY; j++)
	{
	  hz[i*NY + j] = ((DATA_TYPE) (i-9)*(j+4) + 3) / NX;
	}
    }
}


void runFdtd_OMP(DATA_TYPE* _fict_, DATA_TYPE* ex, DATA_TYPE* ey, DATA_TYPE* hz)
{
  int t, i, j;


    for (t=0; t < tmax; t++)
      {

	for (j=0; j < NY; j++)
	  {
	    ey[0*NY + j] = _fict_[t];
	  }


	for (i = 1; i < NX; i++)
	  {
	    for (j = 0; j < NY; j++)
	      {
		ey[i*NY + j] = ey[i*NY + j] - 0.5*(hz[i*NY + j] - hz[(i-1)*NY + j]);
	      }
	  }


	for (i = 0; i < NX; i++)
	  {
	    for (j = 1; j < NY; j++)
	      {
		ex[i*(NY+1) + j] = ex[i*(NY+1) + j] - 0.5*(hz[i*NY + j] - hz[i*NY + (j-1)]);
	      }
	  }


	for (i = 0; i < NX; i++)
	  {
	    for (j = 0; j < NY; j++)
	      {
		hz[i*NY + j] = hz[i*NY + j] - 0.7*(ex[i*(NY+1) + (j+1)] - ex[i*(NY+1) + j] + ey[(i+1)*NY + j] - ey[i*NY + j]);
	      }
	  }
      }

}

int main()
{
  double t_start, t_end;

  DATA_TYPE* _fict_;
  DATA_TYPE* ex;
  DATA_TYPE* ey;
  DATA_TYPE* hz;
  DATA_TYPE* hz_outputFromGpu;

  _fict_ = (DATA_TYPE*)malloc(tmax*sizeof(DATA_TYPE));
  ex = (DATA_TYPE*)malloc(NX*(NY+1)*sizeof(DATA_TYPE));
  ey = (DATA_TYPE*)malloc((NX+1)*NY*sizeof(DATA_TYPE));
  hz = (DATA_TYPE*)malloc(NX*NY*sizeof(DATA_TYPE));
  hz_outputFromGpu = (DATA_TYPE*)malloc(NX*NY*sizeof(DATA_TYPE));



  init_arrays(_fict_, ex, ey, hz);
  init_array_hz(hz_outputFromGpu);

  t_start = rtclock();
  runFdtd_OMP(_fict_, ex, ey, hz_outputFromGpu);
  t_end = rtclock();



  return 0;
}
