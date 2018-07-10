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
#include <string.h>
#include <math.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include "polybenchUtilFuncts.h"

//define the error threshold for the results "not matching"
#define ERROR_THRESHOLD 0.05


/* Problem size */
#define N 2048
#define M 2048

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
//  int i, j;

  /*for (i = 0; i < N; i++) { //Original version contains two seperate loops
                              //it was combined to function as one
    for (j = 0; j < M; j++) {
      C[i][j] *= beta;
    }
  }

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      for (k = 0; k < M; k++) {
	C[i][j] += alpha * A[i][k] * A[j][k];
      }
    }
  }*/
#pragma omp parallel for
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < M; j++) {
      C[i][j] *= beta;
      for(int k=0; k< M; k++) {
	C[i][j] += alpha * A[i][k] * A[j][k];
      }
    }
  }

}

void compareResults() {
  int i,j,fail;
  fail = 0;

  // Compare C with D
  for (i=0; i<N; i++) {
    for (j=0; j<M; j++)	{
      if (percentDiff(C[i][j], D[i][j]) > ERROR_THRESHOLD) {
	fail++;
      }
    }
  }

  // print results
  printf("Non-Matching CPU-GPU Outputs Beyond Error Threshold of %4.2f Percent: %d\n", ERROR_THRESHOLD, fail);
}

void syrkGPU() {
  //int i, j;
  double t_start, t_end;

  t_start = rtclock();

#pragma omp target data map(to: A[0:N][0:M]) map(tofrom: D[0:N][0:M])
#pragma omp target teams
#pragma omp distribute parallel for collapse(2)
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < M; j++) {
      D[i][j] *= beta;
      for(int k=0; k< M; k++) {
	D[i][j] += alpha * A[i][k] * A[j][k];
      }
    }
  }

  t_end = rtclock();
  fprintf(stdout, "GPU Runtime: %0.6lfs\n", t_end - t_start);

}

int main() {
  double t_start, t_end;
  memset(A, 0, N * M * sizeof(float));
  memset(C, 0, N * M * sizeof(float));
  memset(D, 0, N * M * sizeof(float));
  init_arrays();
  syrkGPU();
  t_start = rtclock();
  syrk();
  t_end = rtclock();
  fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_end - t_start);
  compareResults();
  return 0;
}
