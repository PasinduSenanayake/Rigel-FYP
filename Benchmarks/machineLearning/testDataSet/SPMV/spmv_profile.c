/***************************************************************************
 *
 *            (C) Copyright 2010 The Board of Trustees of the
 *                        University of Illinois
 *                         All Rights Reserved
 *
 * SPMV: Sparse-Matrix Dense-Vector Multiplication
 *       Computes the product of a sparse matrix with a dense vector.
 *       The sparse matrix is read from file in coordinate format, converted
 *       to JDS format with configurable padding and alignment for different
 *       devices.
 *
 ***************************************************************************/

/***************************************************************************
 *
 *  This benchmark was adapted to run on GPUs with OpenMP 4.0 pragmas
 *  and OpenCL driver implemented in gpuclang 2.0 (based on clang 3.5)
 *
 *  Marcio M Pereira <mpereira@ic.unicamp.br>
 *
 ***************************************************************************/

/*
 * === NOTE ===
 *
 * The Polyhedral optmizations restricts the class of loops it can manipulate
 * to sequences of imperfectly nested loops with particular constraints on the
 * loop bound and array subscript expressions.
 *
 * To allow this optimization we fixed the problem size with __STATIC__ tag
 * comment this tag to use original version.
 *
 */


#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#include "convert_dataset.h"
#include "parboil.h"
#include "polybenchUtilFuncts.h"

#define ERROR_THRESHOLD 0.05



  // Define statically the problem size
  #define N 146689 //Problem size here, Increasing might lead to a Core dump


/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;

double t_start, t_end, t_start_GPU, t_end_GPU;
float *h_Ax_vector_GPU, *h_Ax_vector_CPU;

void input_vec(char *fName,float *h_vec,int dim)
{
  FILE* fid = fopen(fName, "rb");
  fread (h_vec, sizeof (float), dim, fid);
  fclose(fid);
}

static int generate_vector(float *x_vector, int dim)
{
  srand(54321);
  int i;
  for(i=0;i<dim;i++)
    {
      x_vector[i] = (rand() / (float) RAND_MAX);
    }
  return 0;
}

double spmvCPU(int argc, char** argv) {
  struct pb_Parameters *parameters;

  parameters = pb_ReadParameters(&argc, argv);
  if ((parameters->inpFiles[0] == NULL) || (parameters->inpFiles[1] == NULL))
    {
      fprintf(stderr, "Expecting two input filenames\n");
      exit(-1);
    }

  int len;
  int depth;
  int dim;
  int pad = 1;
  int nzcnt_len;

  float *h_data;
  int *h_indices;
  int *h_ptr;
  int *h_perm;
  int *h_nzcnt;
  //vector
  float *h_Ax_vector;
  float *h_x_vector;

  int col_count;
  coo_to_jds(
	     parameters->inpFiles[0], // bcsstk32.mtx, fidapm05.mtx, jgl009.mtx
	     1, // row padding
	     pad, // warp size
	     1, // pack size
	     1, // is mirrored?
	     0, // binary matrix
	     0, // debug level [0:2]
	     &h_data, &h_ptr, &h_nzcnt, &h_indices, &h_perm,
	     &col_count, &dim, &len, &nzcnt_len, &depth
	     );

  h_Ax_vector=(float*)malloc(sizeof(float)*dim);
  h_x_vector=(float*)malloc(sizeof(float)*dim);
  input_vec( parameters->inpFiles[1],h_x_vector,dim);




  //main execution
  t_start = rtclock();

//Section A to profile

  for(int p=0;p<50;p++)
    {

      for (int i = 0; i < N; i++) {
	float sum = 0.0f;
	int  bound = h_nzcnt[i];
	for( int k=0;k<bound;k++ ) {
	  int j = h_ptr[k] + i;
	  int in = h_indices[j];

	  float d = h_data[j];
	  float t = h_x_vector[in];

	  sum += d*t;
	}
	h_Ax_vector[h_perm[i]] = sum;
      }
    }

//End of Section A to profile

  t_end = rtclock();

  h_Ax_vector_CPU = h_Ax_vector;
  free (h_data);
  free (h_indices);
  free (h_ptr);
  free (h_perm);
  free (h_nzcnt);
  free (h_x_vector);
  pb_FreeParameters(parameters);
  return t_end - t_start;
}

int main(int argc, char** argv) {
  double t_CPU;


  t_CPU = spmvCPU(argc, argv);
  fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_CPU);

  free (h_Ax_vector_CPU);

  return 0;
}
