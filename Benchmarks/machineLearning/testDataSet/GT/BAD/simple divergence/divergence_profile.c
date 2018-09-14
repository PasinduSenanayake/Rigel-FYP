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

typedef float DATA_TYPE;

//----> AdditionalCodeHook

void Divergence_CPU(DATA_TYPE* B){

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

}



int main(int argc, char** argv)
{omp_set_num_threads(1);
  double t_start, t_end, t_start_GPU, t_end_GPU;


  DATA_TYPE* B;

  B = (DATA_TYPE*)malloc(NI*sizeof(DATA_TYPE));

  fprintf(stdout, "<< Initializing Matrices A\n");

  Divergence_CPU(B);
  free(B);
  return 0;
}
