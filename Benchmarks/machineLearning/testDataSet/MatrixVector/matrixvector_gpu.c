
#include <stdio.h>
#include <omp.h>

int main(int argc, char* argv[]) {
  int i,j;

  int N = atoi(argv[1]);
  float *b  = (float *)malloc(sizeof(float)*N);
  float *c = (float *)malloc(sizeof(float)*N);
  float **A = (float **)malloc(N * sizeof(float *));
  for (i=0; i<N; i++){
       A[i] = (float *)malloc(N * sizeof(float));
     }




	// computes A*b
  double startTime = omp_get_wtime();
  #pragma omp target data map(from:A[0:N][0:N]) map(from:b[0:N]) map(tofrom:c[0:N])
  #pragma omp target teams
	#pragma omp distribute parallel for
  for (int i = 0; i <  N; i++){
      for (int j = 0; j < N; j++){
          A[i][j] = i+j;
      }
      b[i] = i;
    }
  #pragma omp target teams
  #pragma omp distribute parallel for
	for (int i=0; i<N; i++) {
		c[i]=0;
		for (int j=0;j<N;j++) {
			c[i]=c[i]+A[i][j]*b[j];
		}
	}
  printf("%f\n",omp_get_wtime()-startTime );


return 0;
}
