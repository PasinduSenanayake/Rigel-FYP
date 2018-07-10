#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

double step;

int main (int argc, const char *argv[]) {

    long int steps = atoi(argv[1]);
    int i;
    double x;
    double pi, sum = 0.0;


    step = 1.0/(double) steps;

    // Compute parallel compute times for 1-MAX_THREADS

        printf(" running on gpu ");

        // This is the beginning of a single PI computation

        sum = 0.0;
        double start = omp_get_wtime();

				#pragma omp target teams map(tofrom:sum)
				#pragma omp distribute parallel for reduction(+:sum)
        for (i=0; i < steps; i++) {
        //  printf("%d\n", omp_get_num_threads() );
            double x = (i+0.5)*step;
            sum += 4.0 / (1.0+x*x);
        }

        // Out of the parallel region, finialize computation
        pi = step * sum;
        double delta = omp_get_wtime() - start;
        printf("PI = %.16g computed in %.4g seconds\n", pi, delta);




}
