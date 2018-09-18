
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

/*
 * This example demonstrates the impact of misaligned reads on performance by
 * forcing misaligned reads to occur on a float*.
 */

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
    #pragma omp parallel for
    for (int k = 0; k < n;k++)
    {
      if ((k*offset)<n)
      {
      C[k] = A[k *offset] + B[k*offset];
      }
    }
}

void sumArraysOnDevice(float *A, float *B, float *C, const int n, int offset)
{
    #pragma omp target data map(to:A[0:n],B[0:n],C[0:n])
    #pragma omp target teams thread_limit(512)
    #pragma omp distribute parallel for schedule(static,1)
    for (int k = 0; k < n; k++)
    {
        if ((k*offset)<n)
        {
        C[k] = A[k *offset] + B[k*offset];
        }
    }
}


int main(int argc, char **argv)
{

    // set up array size
    int nElem = 6400000*256; // total number of elements to reduce
    printf("With array size %d\n", nElem);
    size_t nBytes = nElem * sizeof(float);

    // set up offset for summary
    int offset = 2;

    // allocate host memory
    float *h_A = (float *)malloc(nBytes);
    float *h_B = (float *)malloc(nBytes);
    float *hostRef = (float *)malloc(nBytes);
    float *deviceRef = (float *)malloc(nBytes);

    //  initialize host array
    initialData(h_A, nElem);
    initialData(h_B, nElem);

    //  summary at host side
    double t_start = omp_get_wtime();
    sumArraysOnHost(h_A, h_B, hostRef, nElem, offset);
    printf("Host   %f\n",omp_get_wtime() - t_start );

    t_start = omp_get_wtime();
    sumArraysOnDevice(h_A, h_B, deviceRef, nElem, offset);
    printf("Device %f\n",omp_get_wtime() - t_start );

    free(h_A);
    free(h_B);

return 0;
}
