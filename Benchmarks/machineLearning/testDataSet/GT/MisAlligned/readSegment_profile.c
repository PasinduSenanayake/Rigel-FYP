#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <omp.h>

#include "polybenchUtilFuncts.h"

#define PERCENT_DIFF_ERROR_THRESHOLD 1.0E-8
void initialData(float *ip,  int size)
{
    for (int i = 0; i < size; i++)
    {
        ip[i] = (float)( rand() & 0xFF ) / 100.0f;
    }

    return;
}


void sumArraysOnHost(float *A, float *B, float *C, const int n, int offset)
{
  //section A to profile
    for (int idx = 0; idx < n; idx++ )
    {
      int k = idx + offset;
      if (k<= n) {
        C[k] = A[idx] + B[idx];
      }
    }

  //end of profiling region
}


int main(int argc, char **argv)
{
    int nElem = 1 << 20; // problem size
    int offset = 11;
    size_t nBytes = nElem * sizeof(float);

    float *h_A = (float *)malloc(nBytes);
    float *h_B = (float *)malloc(nBytes);
    float *hostRef = (float *)malloc(nBytes);

    initialData(h_A, nElem);
    sumArraysOnHost(h_A, h_B, hostRef, nElem, offset);


    free(h_A);
    free(h_B);
    free(hostRef);
    return EXIT_SUCCESS;
}
