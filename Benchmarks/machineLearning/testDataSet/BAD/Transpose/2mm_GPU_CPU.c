/**
 * 2mm.c: This file was adapted from PolyBench/GPU 1.0 test suite
 * to run on GPU with OpenMP 4.0 pragmas and OpenCL driver.
 *
 * http://www.cse.ohio-state.edu/~pouchet/software/polybench/GPU
 *
 * Contacts: Marcio M Pereira <mpereira@ic.unicamp.br>
 *           Rafael Cardoso F Sousa <rafael.cardoso@students.ic.unicamp.br>
 *	     Luís Felipe Mattos <ra107822@students.ic.unicamp.br>
*/

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>


/* Problem size. */
# define NI 12000
# define NK 12000


/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;

void init_array(DATA_TYPE* A)
{
  srand(time(0));
  for (int i = 0; i < NI; i++)
    {
      for (int j = 0; j < NK; j++)
	{
	  A[i*NI + j] = ((DATA_TYPE)rand()) / NI;
	}
    }
}

void compareResults(DATA_TYPE *A, DATA_TYPE *B)
{
  int i,j,fail;
  fail = 0;

  for (i=0; i < NI; i++)
    {
      for (j=0; j < NK; j++)
	{
    printf("%f ", A[i*NI + j]);
	}

  printf("\n");
    }

printf("===========================================================================\n");

    for (i=0; i < NI; i++)
      {
        for (j=0; j < NK; j++)
    {
      printf("%f ", B[i*NI + j]);
    }

    printf("\n");
      }

}

//This implementation suffers from non-coalased memeory access
void Tranpose_GPU(DATA_TYPE* A,DATA_TYPE* B){
#pragma omp target data map(to:A[0:NI*NK]) map(tofrom:B[0:NI*NK])
#pragma omp target teams thread_limit(512)
#pragma omp distribute parallel for
for (int i = 0; i < NI; i++)
{
  for (int j = 0; j < NK; j++)
  {
  B[j*NI + i]  = A[i*NI + j] ;
  }
}
}


void Tranpose_CPU(DATA_TYPE* A,DATA_TYPE* C){
#pragma omp parallel for
for (int i = 0; i < NI; i++)
{
  for (int j = 0; j < NK; j++)
  {
  C[j*NI + i]  = A[i*NI + j] ;
  }
}
}


int main(int argc, char** argv)
{
  double t_start, t_end, t_start_GPU, t_end_GPU;

  DATA_TYPE* A;
  DATA_TYPE* B;
  DATA_TYPE* C;

  C = (DATA_TYPE*)malloc(NI*NK*sizeof(DATA_TYPE));
  A = (DATA_TYPE*)malloc(NI*NK*sizeof(DATA_TYPE));
  B = (DATA_TYPE*)malloc(NI*NK*sizeof(DATA_TYPE));


  fprintf(stdout, "<< Initializing Matrices A\n");
  init_array(A);

  t_start_GPU = omp_get_wtime();
  Tranpose_GPU(A,B);
  t_end_GPU = omp_get_wtime();

  printf("GPU threaded %f \n",t_end_GPU - t_start_GPU );

  t_start = omp_get_wtime();
  Tranpose_CPU(A,C);
  t_end = omp_get_wtime();

  printf("CPU threaded %f \n",t_end - t_start);

  //compareResults(B,C);

  free(C);
  free(A);
  free(B);
  return 0;
}
