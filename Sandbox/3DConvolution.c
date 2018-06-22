
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
// Problem size

int NI = 10;
int NJ = 10;
int NK = 10;

 // Can switch DATA_TYPE between float and double
typedef float DATA_TYPE;


//----> AdditionalCodeHook


void init(DATA_TYPE* A)
{
	int i, j, k;

	for (i = 0; i < NI; ++i)
    	{
		for (j = 0; j < NJ; ++j)
		{
			for (k = 0; k < NK; ++k)
			{
				A[i*(NK * NJ) + j*NK + k] = i % 12 + 2 * (j % 7) + 3 * (k % 13);
			}
		}
	}
}

int main()
{
double t_start, t_end;

	DATA_TYPE* A;
	DATA_TYPE* B;

	A = (DATA_TYPE*)malloc(NI*NJ*NK*sizeof(DATA_TYPE));
	B = (DATA_TYPE*)malloc(NI*NJ*NK*sizeof(DATA_TYPE));


	init(A);

	DATA_TYPE c11, c12, c13, c21, c22, c23, c31, c32, c33;

	c11 = +2;  c21 = +5;  c31 = -8;
	c12 = -3;  c22 = +6;  c32 = -9;
	c13 = +4;  c23 = +7;  c33 = +10;

//t_start = omp_get_wtime();

// #pragma omp target data map(to:A[0:NI*NJ*NK]) map(tofrom:B[0:NI*NJ*NK])
// #pragma omp target teams num_teams(512 ) thread_limit(1024)
// #pragma omp distribute

	for (int i = 1; i < NI - 1; ++i) // 0
	{
		for (int j = 1; j < NJ - 1; ++j) // 1
		{
			for (int k = 1; k < NK -1; ++k) // 2
			{
				//printf("Team %d Thread %d Number of threads %d \n", omp_get_team_num() ,omp_get_thread_num(),omp_get_num_threads());
				//printf("i:%d\nj:%d\nk:%d\n", i, j, k);
				B[i*(NK * NJ) + j*NK + k] = c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)] +  c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)] +  c21 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)]+  c23 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)] +  c31 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k - 1)] +  c33 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k - 1)] +  c12 * A[(i + 0)*(NK * NJ) + (j - 1)*NK + (k + 0)]+  c22 * A[(i + 0)*(NK * NJ) + (j + 0)*NK + (k + 0)]+  c32 * A[(i + 0)*(NK * NJ) + (j + 1)*NK + (k + 0)]+  c11 * A[(i - 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]+  c13 * A[(i + 1)*(NK * NJ) + (j - 1)*NK + (k + 1)]+  c21 * A[(i - 1)*(NK * NJ) + (j + 0)*NK + (k + 1)]+  c23 * A[(i + 1)*(NK * NJ) + (j + 0)*NK + (k + 1)] +  c31 * A[(i - 1)*(NK * NJ) + (j + 1)*NK + (k + 1)]+  c33 * A[(i + 1)*(NK * NJ) + (j + 1)*NK + (k + 1)];
			}
		}
	}

//#pragma omp target update from(B)

//t_end = omp_get_wtime();
printf("Time spent %lf\n",t_end-t_start );

free(A);
free(B);

// #pragma  omp parallel for collapse(2)
// 	for(int i =0;i<100;i++){
// 	    for(int k=0;k<50;k++) {
//           //  printf("Thread id %d iteration number %d\n", omp_get_thread_num(), i);
//         }
// 	}

    	return 0;
}
