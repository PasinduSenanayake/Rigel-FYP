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


void Tranpose_GPU(DATA_TYPE* A,DATA_TYPE* B){

//Section A region to profle
for (int i = 0; i < NI; i++)
{
  for (int j = 0; j < NK; j++)
  {
  B[j*NI + i]  = A[i*NI + j] ;
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

  A = (DATA_TYPE*)malloc(NI*NK*sizeof(DATA_TYPE));
  B = (DATA_TYPE*)malloc(NI*NK*sizeof(DATA_TYPE));


  fprintf(stdout, "<< Initializing Matrices A\n");
  init_array(A);


  Tranpose_GPU(A,B);

  free(A);
  free(B);
  return 0;
}
