#include <stdio.h>
#include <omp.h>
#include <math.h>

void isprime(long long num);
int main(){

  omp_set_num_threads(10);

  double startTime = omp_get_wtime( );
  printf("||| \n" );
  #pragma omp parallel
  {
  int i = omp_get_thread_num() + 1;
  long long start = 1000000000 * i;
  long long end = 1000000000 *(i + 1) -1;
  long long j;
  for (j = start ; start<= end; j++) {
    /* code */
    isprime(start);
  }

  double endTime = omp_get_wtime( );
  printf("diff = %.16g  thread number: %d ", endTime - startTime,omp_get_thread_num());
}
  return 0;
}

void isprime(long long num){
  long long i;
  int FLAG=1;
  for(i=2;i<=sqrt(num);i++)
  {
     if(num%i == 0)
     {
        FLAG = 0;
        break;
     }
  }
}
