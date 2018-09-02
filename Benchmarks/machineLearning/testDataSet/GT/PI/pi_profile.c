#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

double step;


//----> AdditionalCodeHook

int main (int argc, const char *argv[]) {

    long int steps = 99999999;
    int i;
    double x;
    double pi, sum = 0.0;


    step = 1.0/(double) steps;


        sum = 0.0;




        for (i=0; i < steps; i++) {

            double x = (i+0.5)*step;
            sum += 4.0 / (1.0+x*x);
        }




        pi = step * sum;




}
