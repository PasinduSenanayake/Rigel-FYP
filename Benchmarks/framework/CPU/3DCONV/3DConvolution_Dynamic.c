/**
 * 3DConvolution.c: This file was adapted from PolyBench/GPU 1.0 test suite
 * to run on GPU with OpenMP 4.0 pragmas and OpenCL driver.
 *
 * http://www.cse.ohio-state.edu/~pouchet/software/polybench/GPU
 *
 * Contacts: Marcio M Pereira <mpereira@ic.unicamp.br>
 *           Rafael Cardoso F Sousa <rafael.cardoso@students.ic.unicamp.br>
 *	     Luís Felipe Mattos <ra107822@students.ic.unicamp.br>
 */

#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <omp.h>

#include "./polybenchUtilFuncts.h"

//define the error threshold for the results "not matching"
#define ERROR_THRESHOLD 0.5

/* Problem size */
#define NI 512
#define NJ 512
#define NK 512

/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;

void conv3D_OMP(DATA_TYPE* A, DATA_TYPE* B)
{
  DATA_TYPE c11, c12, c13, c21, c22, c23, c31, c32, c33;

  c11 = +2;  c21 = +5;  c31 = -8;
  c12 = -3;  c22 = +6;  c32 = -9;
  c13 = +4;  c23 = +7;  c33 = +10;

  #pragma omp parallel for schedule(dynamic)
  for (int j = 1; j < NJ - 1; ++j)
  {
    for (int i = 1; i < NI - 1; ++i)
    {
      for (int k = 1; k < NK -1; ++k)
      {
        B[i*(NK * NJ) + j*NK + k] = c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
          +   c21 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c23 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
          +   c31 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]  +  c33 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]
          +   c12 * A[(i + 0)*(NK * NJ) + (j - 1)*NK + (k + 0)]  +  c22 * A[(i + 0)*(NK * NJ) + (j + 0)*NK + (k + 0)]
          +   c32 * A[(i + 0)*(NK * NJ) + (j + 1)*NK + (k + 0)]  +  c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]
          +   c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]  +  c21 * A[(i - 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]
          +   c23 * A[(i + 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]  +  c31 * A[(i - 1)*(NK * NJ) + (j + 1)*NK + (k + 1)]
          +   c33 * A[(i + 1)*(NK * NJ) + (j + 1)*NK + (k + 1)];
      }
    }
  }

  //end of region to profile
}

void init(DATA_TYPE* A)
{
  int i, j, k;

  for (i = 0; i < NI; ++i)
  {
    for (j = 0; j < NJ; ++j)
    {
      for (k = 0; k < NK; ++k)
      {
        A[i*(NK * NJ) + j*NK + k] = i % 12 + 2 * (j % 7) + 3 * (k % 13);
      }
    }
  }
}

//----> AdditionalCodeHook

int main(int argc, char *argv[])
{
  double t_start, t_end;

  DATA_TYPE* A;
  DATA_TYPE* B_GPU;

  A = (DATA_TYPE*)malloc(NI*NJ*NK*sizeof(DATA_TYPE));
  B_GPU = (DATA_TYPE*)malloc(NI*NJ*NK*sizeof(DATA_TYPE));

  fprintf(stdout, ">> Three dimensional (3D) convolution <<\n");

  init(A);

  t_start = rtclock();
  conv3D_OMP(A, B_GPU);
  t_end = rtclock();
  fprintf(stdout, "Runtime Dynamic CoreTest: %0.6lfs\n", t_end - t_start);


  free(A);
  free(B_GPU);

  return 0;
}
