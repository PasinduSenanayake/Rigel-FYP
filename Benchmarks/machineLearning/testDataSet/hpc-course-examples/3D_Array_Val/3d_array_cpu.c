#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>


#define N 700

float a[N][N][N];

int main (int argc, char *argv[])
{


double startTime = omp_get_wtime();
#pragma omp parallel for schedule(static)
{
    for (int ii=0; ii<N; ii++) {
      for (int jj=0;jj<N; jj++) {
          for (int kk=0;kk<N; kk++) {
             float tmp = exp((float)kk) * exp((float)jj) / exp((float)ii); /* use some CPU cycles */
              a[ii][jj][kk] = 9*tmp;  /* initialise */
           }
        }
    }
}

printf("%f\n",omp_get_wtime()-startTime );



  /* tests */
  // for (int ii=0; ii<N; ii++) {
  //   for (int jj=0;jj<N; jj++) {
  //     for (int kk=0;kk<N; kk++) {
  //       float tmp = exp((float)kk) * exp((float)jj) / exp((float)ii);
	// if (a[ii][jj][kk] != 9*tmp) {
  //   printf("cell:%f\n", 9*tmp);
	//   printf("Error, we missed a cell: a[%d][%d][%d] = %f\n", ii, jj, kk, a[ii][jj][kk]);
	// }
  //     }
  //   }
  // }

  return EXIT_SUCCESS;
}
