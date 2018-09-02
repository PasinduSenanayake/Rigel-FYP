
#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <omp.h>

#include "polybenchUtilFuncts.h"

#define GPU 1

//define the error threshold for the results "not matching"
#define PERCENT_DIFF_ERROR_THRESHOLD 0.05

int NI = 2048;
int NJ = 2048;
int NK = 2048;

int ALPHA = 32412.0f;
int BETA = 2123.0f;

typedef float DATA_TYPE;



//----> AdditionalCodeHook

void gemm(DATA_TYPE *A, DATA_TYPE *B, DATA_TYPE *C)
{



  for (int i = 0; i < 204; i++)
  {
    for (int j = 0; j < NJ; j++)
    {
      C[i*NJ + j] *= BETA;

      for (int k = 0; k < NK; ++k)
      {
        C[i*NJ + j] += ALPHA * A[i*NK + k] * B[k*NJ + j];
      }
    }
  }



}


void init(DATA_TYPE *A, DATA_TYPE *B, DATA_TYPE *C)
{
  int i, j;

  for (i = 0; i < NI; i++)
  {
    for (j = 0; j < NK; j++)
    {
      A[i*NK + j] = ((DATA_TYPE) i*j) / NI;
    }
  }

  for (i = 0; i < NK; i++)
  {
    for (j = 0; j < NJ; j++)
    {
      B[i*NJ + j] = ((DATA_TYPE) i*j + 1) / NJ;
    }
  }

  for (i = 0; i < NI; i++)
  {
    for (j = 0; j < NJ; j++)
    {
      C[i*NJ + j] = ((DATA_TYPE) i*j + 2) / NJ;
    }
  }
}




int main(int argc, char *argv[])
{
  double t_start, t_end;

  DATA_TYPE* A;
  DATA_TYPE* B;
  DATA_TYPE* C;

  A = (DATA_TYPE*)malloc(NI*NK*sizeof(DATA_TYPE));
  B = (DATA_TYPE*)malloc(NK*NJ*sizeof(DATA_TYPE));
  C = (DATA_TYPE*)malloc(NI*NJ*sizeof(DATA_TYPE));

  fprintf(stdout, "<< Matrix-multiply C=alpha.A.B+beta.C >>\n");

  init(A, B, C);

  gemm(A, B, C);


  free(A);
  free(B);
  free(C);

  return 0;
}
