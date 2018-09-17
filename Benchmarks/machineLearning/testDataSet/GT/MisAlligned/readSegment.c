#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <omp.h>

#include "polybenchUtilFuncts.h"

#define PERCENT_DIFF_ERROR_THRESHOLD 1.0E-8

void compareResults(float *z, float *z_outputFromGpu,int n)
{
  int fail = 0;

  for (int i=0; i<n; i++)
  {
    if (percentDiff(z[i], z_outputFromGpu[i]) > PERCENT_DIFF_ERROR_THRESHOLD)
    {
     printf("%f %f\n", z[i] ,z_outputFromGpu[i]);
      fail++;
    }
  }
  printf("Non-Matching CPU-GPU Outputs Beyond Error Threshold of %4.2f Percent: %d\n", PERCENT_DIFF_ERROR_THRESHOLD, fail);
}

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
    for (int idx = 0; idx < n; idx++ )
    {
      int k = idx + offset;
      if (k<= n) {
        C[k] = A[idx] + B[idx];
      }
    }
}

void sumArraysOnDevice(float *A, float *B, float *C, const int n, int offset)
{
  #pragma omp target data map(to:A[0:n]) map(to:B[0:n]) map(tofrom:C[0:n])
  #pragma omp target teams thread_limit(256)
  #pragma omp distribute parallel for schedule(static,1)
    for (int idx = 0; idx < n; idx++)
    {
        int k = idx + offset;
        if (k<= n) {
          C[k] = A[idx] + B[idx];
        }
    }
}

int main(int argc, char **argv)
{
  double t_start_OMP,t_end_OMP,t_start_GPU,t_end_GPU;

    int nElem = 1 << 27; // total number of elements to reduce
    int offset = 11;
    size_t nBytes = nElem * sizeof(float);

    float *h_A = (float *)malloc(nBytes);
    float *h_B = (float *)malloc(nBytes);
    float *hostRef = (float *)malloc(nBytes);
    float *deviceRef = (float *)malloc(nBytes);

    initialData(h_A, nElem);

    t_start_OMP = omp_get_wtime();
    sumArraysOnHost(h_A, h_B, hostRef, nElem, offset);
    t_end_OMP = omp_get_wtime();
    fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_end_OMP - t_start_OMP);//);


    t_start_GPU = omp_get_wtime();
    sumArraysOnDevice(h_A, h_B, deviceRef, nElem, offset);
    t_end_GPU = omp_get_wtime();

    fprintf(stdout, "GPU Runtime: %0.6lfs\n", t_end_GPU - t_start_GPU);//);

    compareResults(hostRef,deviceRef,nElem);

    free(h_A);
    free(h_B);
    free(hostRef);
    return EXIT_SUCCESS;
}
