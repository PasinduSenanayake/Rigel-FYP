#include <stdio.h>
#include <omp.h>


int main (int argc, char *argv[])
{
  int N = atoi(argv[1]);
  int  i,j;
  long int a = 0;
  double start = omp_get_wtime();
  #pragma omp parallel for private(i ,j) reduction(+:a)
  {
  for (j = 0; j < N; j++) {
    for (i = 0; i < N; i++) {
        a += i*j;
    }
  }
  }

  printf("%f\n", omp_get_wtime()-start );
  printf("%ld\n",a );
  return 0;
}
