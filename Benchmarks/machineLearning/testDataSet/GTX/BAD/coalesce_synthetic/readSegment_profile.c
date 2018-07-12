
#include <stdio.h>
#include <stdlib.h>

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
  //section A start profile here
    for (int k = 0; k < n;k++)
    {
      if ((k*offset)<n)
      {
      C[k] = A[k *offset] + B[k*offset];
      }
    }
  //end of section A profile
}

//----> AdditionalCodeHook

int main(int argc, char **argv)
{

    // set up array size
    int nElem = 6400000; // total number of elements to reduce
    // set up offset for summary
    int offset = 2;
    printf("With array size %d\n", nElem);
    size_t nBytes = nElem * sizeof(float);



    // allocate host memory
    float *h_A = (float *)malloc(nBytes);
    float *h_B = (float *)malloc(nBytes);
    float *hostRef = (float *)malloc(nBytes);

    //  initialize host array
    initialData(h_A, nElem);
    initialData(h_B, nElem);

    sumArraysOnHost(h_A, h_B, hostRef, nElem, offset);

    free(h_A);
    free(h_B);
    free(hostRef);
return 0;
}
