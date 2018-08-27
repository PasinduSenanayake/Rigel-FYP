/**
 * mvt.c: This file was adapted from PolyBench/GPU 1.0 test suite
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

#include "polybenchUtilFuncts.h"

#define PERCENT_DIFF_ERROR_THRESHOLD 0.05

int N = 8192;

typedef float DATA_TYPE;

//----> AdditionalCodeHook

void init_array(DATA_TYPE* A, DATA_TYPE* x1, DATA_TYPE* x2, DATA_TYPE* y, DATA_TYPE* y2)
{
  int i, j;

  for (i = 0; i < N; i++)
  {
    x1[i] = ((DATA_TYPE) i) / N;
    x2[i] = ((DATA_TYPE) i + 1) / N;
    y[i] = ((DATA_TYPE) i + 3) / N;
    y2[i] = ((DATA_TYPE) i + 4) / N;
    for (j = 0; j < N; j++)
    {
      A[i*N + j] = ((DATA_TYPE) i*j) / N;
    }
  }
}


void runMvt(DATA_TYPE* a, DATA_TYPE* x1, DATA_TYPE* x2, DATA_TYPE* y, DATA_TYPE* y2)
{



  for (int i=0; i<N; i++)
  {
    for (int j=0; j<N; j++)
    {
      x1[i] = x1[i] + a[i*N + j] * y[j];
      x2[i] = x2[i] + a[j*N + i] * y2[j];

    }
  }



}






int main()
{
  double t_start, t_end;

  DATA_TYPE* a;
  DATA_TYPE* x1;
  DATA_TYPE* x2;
  DATA_TYPE* y_1;
  DATA_TYPE* y_2;

  a = (DATA_TYPE*)malloc(N*N*sizeof(DATA_TYPE));
  x1 = (DATA_TYPE*)malloc(N*sizeof(DATA_TYPE));
  x2 = (DATA_TYPE*)malloc(N*sizeof(DATA_TYPE));
  y_1 = (DATA_TYPE*)malloc(N*sizeof(DATA_TYPE));
  y_2 = (DATA_TYPE*)malloc(N*sizeof(DATA_TYPE));

  init_array(a, x1, x2, y_1, y_2);

  t_start = rtclock();
  //run the algorithm on the CPU
  runMvt(a, x1, x2, y_1, y_2);
  t_end = rtclock();



  free(a);
  free(x1);
  free(x2);
  free(y_1);
  free(y_2);

  return 0;
}
