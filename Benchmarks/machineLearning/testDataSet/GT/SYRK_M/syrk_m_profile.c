/**
 * syrk_m.c: This file was adapted from PolyBench/GPU 1.0 test suite
 * to run on GPU with OpenMP 4.0 pragmas and OpenCL driver.
 *
 * http://www.cse.ohio-state.edu/~pouchet/software/polybench/GPU
 *
 * Contact: Marcio M Pereira <mpereira@ic.unicamp.br>
 *          Rafael Cardoso F Sousa <rafael.cardoso@students.ic.unicamp.br>
 *          Luís Felipe Mattos <ra107822@students.ic.unicamp.br>
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include "polybenchUtilFuncts.h"

//define the error threshold for the results "not matching"
#define ERROR_THRESHOLD 0.05
#define GPU_DEVICE 1

/* Problem size */
#define N 1024
#define M 1024

/* Declared constant values for alpha and beta */
/* (same as values in PolyBench 2.0) */
#define alpha 12435
#define beta 4546

/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;

DATA_TYPE A[N][M];
DATA_TYPE C[N][M];
DATA_TYPE D[N][M];

void init_arrays() {
  int i, j;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      A[i][j] = ((DATA_TYPE) i*j) / N;
    }
    for (j = 0; j < M; j++) {
      C[i][j] = ((DATA_TYPE) i*j + 2) / N;
      D[i][j] = C[i][j];
    }
  }
}

void syrk() {

  //Section A profile here
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < M; j++) {
      C[i][j] *= beta;
      int k;
      for(k=0; k< M; k++) {
	C[i][j] += alpha * A[i][k] * A[j][k];
      }
    }
  }

  //End of section A profiling

}

//----> AdditionalCodeHook

int main() {
  double t_start, t_end;

  init_arrays();

  t_start = rtclock();
  syrk();
  t_end = rtclock();
  fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_end - t_start);

  return 0;
}
