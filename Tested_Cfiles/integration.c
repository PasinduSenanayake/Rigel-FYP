#include<stdio.h>
#include<omp.h>

static long num_steps = 1000;
double step;

int main(void)
{
  int i;
  double x,pi,sum=0.0;

  step =1.0/(double)num_steps;

double first = omp_get_wtime();

#pragma omp parallel
{
  for(i=0;i<num_steps;i++){
    x = (i+0.5)*step;

    sum = sum + 4.0/(1.0+x*x);
  }
}

double last = omp_get_wtime();
 pi = step*sum;

 printf("pi %f\n", pi);
}
