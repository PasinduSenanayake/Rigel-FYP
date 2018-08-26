#include <omp.h>
#include <stdio.h>
#include <stdlib.h>


double step;

int main (int argc, const char *argv[]) {
    long int steps = atoi(argv[1]);
    int i,j;
    double x;
    double pi, sum = 0.0;


    step = 1.0/(double) steps;

//----> AdditionalCodeHook    




        sum = 0.0;
        double start = omp_get_wtime();


        for (i=0; i < steps; i++) {
            double x = (i+0.5)*step;
            sum += 4.0 / (1.0+x*x);
        }

        pi = step * sum;
        double delta = omp_get_wtime() - start;

}
