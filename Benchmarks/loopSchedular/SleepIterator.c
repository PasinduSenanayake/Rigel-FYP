#include <unistd.h>
#include <stdlib.h>
#include <omp.h>
#include <stdio.h>

#define THREADS 4
#define N 16

int main ( ) {
  int i;

  #pragma omp parallel for schedule(static) num_threads(THREADS)
  for (i=0; i<N; i++) {
//for(i = 0; i < N; i++){
    sleep(i);
    printf("Thread %d has completed iteration %d.\n", omp_get_thread_num( ), i);
  }

  printf("All done!\n");
  return 0;
}
