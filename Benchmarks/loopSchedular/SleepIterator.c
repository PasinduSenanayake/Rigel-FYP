#include <unistd.h>
#include <stdlib.h>
#include <omp.h>
#include <stdio.h>

int main (int argc, char **argv) {
  int N = strtol(argv[1], NULL, 10);
  #pragma omp parallel for schedule(static)
  for (int i=0; i<N; i++) {
    sleep(i);
    printf("Thread %d has completed iteration %d.\n", omp_get_thread_num( ), i);
  }

  printf("All done!\n");
  return 0;
}
