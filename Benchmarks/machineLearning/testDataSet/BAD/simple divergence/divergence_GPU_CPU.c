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
#include <time.h>
#include <omp.h>


/* Problem size. */
# define NI 64000000*2

/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;

void Divergence_GPU(DATA_TYPE* A){

//Section A region to profle
#pragma omp target data map(to:A[0:NI])
#pragma omp target teams thread_limit(512)
#pragma omp distribute parallel for schedule(static,1)
for (int i = 0; i < NI; i++)
{
  if(i%2==0){
    A[i] = 100.0f;
  }
  else{
    A[i] =  200.0f;
  }
}

//end of Section A region to profile
}

void Divergence_CPU(DATA_TYPE* B){

//Section A region to profle
#pragma omp parallel for
for (int i = 0; i < NI; i++)
{
  if(i%2==0){
    B[i] = 100.0f;
  }
  else{
    B[i] =  200.0f;
  }
}

//end of Section A region to profile
}

//----> AdditionalCodeHook

int main(int argc, char** argv)
{
  double t_start, t_end, t_start_GPU, t_end_GPU;

  DATA_TYPE* A;
  DATA_TYPE* B;

  A = (DATA_TYPE*)malloc(NI*sizeof(DATA_TYPE));
  B = (DATA_TYPE*)malloc(NI*sizeof(DATA_TYPE));

  fprintf(stdout, "<< Initializing Matrices A\n");

t_start_GPU =  omp_get_wtime();
  Divergence_GPU(A);
t_end_GPU = omp_get_wtime();

printf("GPU %f\n",t_end_GPU - t_start_GPU );


  t_start =  omp_get_wtime();
Divergence_CPU(B);
  t_end = omp_get_wtime();

  printf("CPU %f\n",t_end - t_start );

  free(A);
  free(B);
  return 0;
}
