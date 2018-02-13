
#include <omp.h>
#include <stdio.h>
#define N 1000
#define chunk_size 100

int main() {
  int res = 0;
  int i = 0;
  #pragma omp target data
  #pragma omp target
  for (i = 0; i < N; i++) {
    res = res + i;
  }
  printf("%d\n", res);
}
