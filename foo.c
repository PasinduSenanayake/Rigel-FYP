#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>
#include <omp.h>
#include <unistd.h>


double start, finish;
int sleepTime;
void functionone(){
  sleep(sleepTime);
}


void functiontwo() {
  sleep(sleepTime);
}

void functionthree() {
  sleep(sleepTime);
}
int main(int argc, char **argv){
sleepTime = (int)strtol(argv[1], NULL, 10);
start = omp_get_wtime();
#pragma omp parallel

{


  #pragma omp sections
  {
    #pragma omp section
    functionone();
    #pragma omp section
    functiontwo();
    #pragma omp section
    functionthree();
  }
}

finish  = omp_get_wtime();


printf("Time taken for the process %f\n", (finish - start));

}
