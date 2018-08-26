
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>
#include <string.h>
#include <time.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include "./mgbenchUtilFunctions.h"

// #define SIZE 2000000
// #define SIZE2 5000
// #define SIZE 1000000
// #define SIZE2 5000
// #define SIZE 3000000
// #define SIZE2 5000
#define SIZE 4000000
#define SIZE2 5000
#define GPU_DEVICE 0
#define PERCENT_DIFF_ERROR_THRESHOLD 0.01

/// initialize the two strings
void init(char *frase, char *palavra)
{
  int i;
  for(i=0;i<SIZE;i++)
  {
    frase[i] = 'a';
  }

  frase[i] = '\0';
  for(i=0;i<SIZE2;i++)
  {
    palavra[i] = 'a';
  }

  palavra[i] = '\0';
}

/// string matching algorithm GPU
/// s = size of longer string
/// p = size of less string
int string_matching_GPU(char *frase, char *palavra)
{
  int i,diff,j,parallel_size, count = 0;
  diff  = SIZE - SIZE2;


    for(int i=0;i<diff;i++)
    {
      int v;
      v = 1;
      for(int j=0;j<SIZE2;j++)
      {
        if(frase[(i+j)]!=palavra[j])
        {
          v = 0;
        }
      }

      count +=v;

    }
  return count;
}




int main(int argc, char *argv[])
{
  double t_start, t_end;
  char *frase;
  char *palavra;

  int count_cpu, count_gpu;

  frase = (char *) malloc(sizeof(char) * (SIZE+1));
  palavra = (char *) malloc(sizeof(char) * (SIZE2+1));

  init(frase, palavra);


  t_start = rtclock();
  count_gpu = string_matching_GPU(frase, palavra);
  t_end = rtclock();


  free(frase);
  free(palavra);

  return 0;
}
