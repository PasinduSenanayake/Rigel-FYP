/**
 * syr2k.c: This file was adapted from PolyBench/GPU 1.0 test suite
 * to run on GPU with OpenMP 4.0 pragmas and OpenCL driver.
 *
 * http://www.cse.ohio-state.edu/~pouchet/software/polybench/GPU
 *
 * Contacts: Marcio M Pereira <mpereira@ic.unicamp.br>
 *           Rafael Cardoso F Sousa <rafael.cardoso@students.ic.unicamp.br>
 *           Luís Felipe Mattos <ra107822@students.ic.unicamp.br>
 */

#include <assert.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>

#include "polybenchUtilFuncts.h"

// define the error threshold for the results "not matching"
#define PERCENT_DIFF_ERROR_THRESHOLD 0.10

/* Problem size */
#define N 1024
#define M 1024
/* Declared constant values for ALPHA and BETA (same as values in PolyBench 2.0)
 */
#define ALPHA 12435
#define BETA 4546

/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;

void init_arrays(DATA_TYPE *A, DATA_TYPE *B, DATA_TYPE *C) {
  int i, j;

  for (i = 0; i < N; i++) {
    for (j = 0; j < N; j++) {
      C[i * N + j] = ((DATA_TYPE)i * j + 2) / N;
    }

    for (j = 0; j < M; j++) {
      A[i * N + j] = ((DATA_TYPE)i * j) / N;
      B[i * N + j] = ((DATA_TYPE)i * j + 1) / N;
    }
  }
}

void syr2k(DATA_TYPE *A, DATA_TYPE *B, DATA_TYPE *C) {


  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      C[i * N + j] *= BETA;
    }
  }

  //Section A
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      for (int k = 0; k < M; k++) {
        C[i * N + j] += ALPHA * A[i * M + k] * B[j * M + k];
        C[i * N + j] += ALPHA * B[i * M + k] * A[j * M + k];
      }
    }
  }
//end of Section A

}


int main() {
  double t_start, t_end;

  DATA_TYPE *A;
  DATA_TYPE *B;
  DATA_TYPE *C;
  DATA_TYPE *C_Gpu;

  A = (DATA_TYPE *)malloc(N * M * sizeof(DATA_TYPE));
  B = (DATA_TYPE *)malloc(N * M * sizeof(DATA_TYPE));
  C = (DATA_TYPE *)malloc(N * M * sizeof(DATA_TYPE));


  fprintf(stdout, "<< Symmetric rank-2k operations >>\n");

  init_arrays(A, B, C);

  t_start = rtclock();
  syr2k(A, B, C);
  t_end = rtclock();
  fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_end - t_start);

  free(A);
  free(B);
  free(C);

  return 0;
}
