#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>


int N =700;

float a[700][700][700];

//----> AdditionalCodeHook


int main (int argc, char *argv[])
{


  #pragma omp parallel for
    for (int ii=0; ii<N; ii++) {
      for (int jj=0;jj<N; jj++) {
        int piyu;
          for (int kk=0;kk<N; kk++) {
             float tmp = exp((float)kk) * exp((float)jj) / exp((float)ii); /* use some CPU cycles */
              a[ii][jj][kk] = 9*tmp;  /* initialise */
           }
        }
    }


  return EXIT_SUCCESS;
}
