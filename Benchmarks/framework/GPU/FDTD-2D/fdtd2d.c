/**
 * fdtd2d.c: This file was adapted from PolyBench/GPU 1.0 test suite
 * to run on GPU with OpenMP 4.0 pragmas and OpenCL driver.
 *
 * http://www.cse.ohio-state.edu/~pouchet/software/polybench/GPU
 *
 * Contacts: Marcio M Pereira <mpereira@ic.unicamp.br>
 *           Rafael Cardoso F Sousa <rafael.cardoso@students.ic.unicamp.br>
 *           Luís Felipe Mattos <ra107822@students.ic.unicamp.br>
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include <omp.h>

#include "./polybenchUtilFuncts.h"



#define tmax 65536*8
#define NX 32
#define NY 32

typedef float DATA_TYPE;

//----> AdditionalCodeHook


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


void runFdtd(DATA_TYPE* _fict_, DATA_TYPE* ex, DATA_TYPE* ey, DATA_TYPE* hz)
{
  int t, i, j;
  #pragma omp  parallel for private(t,i,j)
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

  DATA_TYPE* _fict_;
  DATA_TYPE* ex;
  DATA_TYPE* ey;
  DATA_TYPE* hz;


  _fict_ = (DATA_TYPE*)malloc(tmax*sizeof(DATA_TYPE));
  ex = (DATA_TYPE*)malloc(NX*(NY+1)*sizeof(DATA_TYPE));
  ey = (DATA_TYPE*)malloc((NX+1)*NY*sizeof(DATA_TYPE));
  hz = (DATA_TYPE*)malloc(NX*NY*sizeof(DATA_TYPE));

  init_arrays(_fict_, ex, ey, hz);

  runFdtd(_fict_, ex, ey, hz);


  return 0;
}
