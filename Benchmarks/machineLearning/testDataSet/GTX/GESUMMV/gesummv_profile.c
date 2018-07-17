/**
 * gesummv.c: This file was adapted from PolyBench/GPU 1.0 test
 * suite to run on GPU with OpenMP 4.0 pragmas and OpenCL driver.
 *
 * http://www.cse.ohio-state.edu/~pouchet/software/polybench/GPU
 *
 * Contacts: Marcio M Pereira <mpereira@ic.unicamp.br>
 *           Rafael Cardoso F Sousa <rafael.cardoso@students.ic.unicamp.br>
 *           Luís Felipe Mattos <ra107822@students.ic.unicamp.br>
 */

#include <omp.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>

#include "polybenchUtilFuncts.h"

// define the error threshold for the results "not matching"
#define PERCENT_DIFF_ERROR_THRESHOLD 0.05


/* Problem size */
#define N 16384

/* Declared constant values for ALPHA and BETA (same as values in PolyBench 2.0)
 */
#define ALPHA 43532.0f
#define BETA 12313.0f

/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;

void gesummv(DATA_TYPE *A, DATA_TYPE *B, DATA_TYPE *x, DATA_TYPE *y) {

//region to profile
  for (int i = 0; i < N; i++) {
    DATA_TYPE tmp = 0;
    y[i] = 0;
    for (int j = 0; j < N; j++) {
      tmp = A[i * N + j] * x[j] + tmp;
      y[i] = B[i * N + j] * x[j] + y[i];
    }
    y[i] = ALPHA * tmp + BETA * y[i];
  }

//end of profiling region
}


void init(DATA_TYPE *A, DATA_TYPE *B, DATA_TYPE *x) {
  int i, j;

  for (i = 0; i < N; i++) {
    x[i] = ((DATA_TYPE)i) / N;

    for (j = 0; j < N; j++) {
      A[i * N + j] = ((DATA_TYPE)i * j) / N;
      B[i * N + j] = ((DATA_TYPE)i * j) / N;
    }
  }
}

//----> AdditionalCodeHook


int main(int argc, char *argv[]) {
  double t_start, t_end;

  DATA_TYPE *A;
  DATA_TYPE *B;
  DATA_TYPE *x;
  DATA_TYPE *y;


  A = (DATA_TYPE *)malloc(N * N * sizeof(DATA_TYPE));
  B = (DATA_TYPE *)malloc(N * N * sizeof(DATA_TYPE));
  x = (DATA_TYPE *)malloc(N * sizeof(DATA_TYPE));
  y = (DATA_TYPE *)malloc(N * sizeof(DATA_TYPE));


  fprintf(stdout, "<< Scalar, Vector and Matrix Multiplication >>\n");

  init(A, B, x);



  init(A, B, x);

  t_start = rtclock();
  gesummv(A, B, x, y);
  t_end = rtclock();
  fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_end - t_start);

  free(A);
  free(B);
  free(x);
  free(y);

  return 0;
}
