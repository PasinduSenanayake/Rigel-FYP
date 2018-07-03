/**
 * atax.c: This file was adapted from PolyBench/GPU 1.0 test suite
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
#include <math.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include <omp.h>

#include "polybenchUtilFuncts.h"

// define the error threshold for the results "not matching"
#define PERCENT_DIFF_ERROR_THRESHOLD 0.5

/* Problem size. */
#define NX 8192
#define NY 8192

#define GPU 1

#ifndef M_PI
#define M_PI 3.14159
#endif

/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;

void init_array(DATA_TYPE *x, DATA_TYPE *A) {
    int i, j;

    for (i = 0; i < NX; i++) {
        x[i] = i * M_PI;
        for (j = 0; j < NY; j++) {
            A[i * NY + j] = ((DATA_TYPE)i * (j)) / NX;
        }
    }
}

void atax_cpu(DATA_TYPE *A, DATA_TYPE *x, DATA_TYPE *y, DATA_TYPE *tmp) {

    for (int i = 0; i < NY; i++) {
        y[i] = 0;
    }

//region to profile
    for (int i = 0; i < NX; i++) {
        tmp[i] = 0;

        for (int j = 0; j < NY; j++) {
            tmp[i] = tmp[i] + A[i * NY + j] * x[j];
        }

        for (int j = 0; j < NY; j++) {
            y[j] = y[j] + A[i * NY + j] * tmp[i];
        }
    }

//end of profiling region

}

//----> AdditionalCodeHook

int main(int argc, char **argv) {
    double t_start, t_end;

    DATA_TYPE *A;
    DATA_TYPE *x;
    DATA_TYPE *y;
    DATA_TYPE *y_outputFromGpu;
    DATA_TYPE *tmp;

    A = (DATA_TYPE *)malloc(NX * NY * sizeof(DATA_TYPE));
    x = (DATA_TYPE *)malloc(NY * sizeof(DATA_TYPE));
    y = (DATA_TYPE *)malloc(NY * sizeof(DATA_TYPE));
    tmp = (DATA_TYPE *)malloc(NX * sizeof(DATA_TYPE));

    fprintf(stdout, "<< Matrix Transpose and Vector Multiplication >>\n");

    init_array(x, A);

    t_start = rtclock();
    atax_cpu(A, x, y, tmp);
    t_end = rtclock();
    fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_end - t_start);

    free(A);
    free(x);
    free(y);
    free(tmp);

    return 0;
}
