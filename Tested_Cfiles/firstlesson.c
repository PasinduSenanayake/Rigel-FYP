#include <omp.h>
#include <stdio.h>



void sayHello (int tid){
  printf("Hello World form Threads %d\n", tid);
}
int main (void){
  int tid = 0;
  printf("%d is the tid value here\n" , tid);
  #pragma omp parallel private(tid) num_threads(20)
  {
    tid = omp_get_thread_num();
      if(tid%2==0){
        sayHello(tid);
      }
  }

  #pragma omp parallel private(tid) num_threads(10)
  {
    tid = omp_get_thread_num();
      if(tid%2==0){
        printf("Hello World form Threads %d\n", tid);
      }
  }
  return 0;
}
