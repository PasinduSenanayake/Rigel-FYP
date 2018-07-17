#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <mm_malloc.h>  

double omp_get_wtime(void); 

void* _mm_malloc (size_t size, size_t align );

// #pragma omp declare simd simdlen(4) notinbranch
// double method(double a, double b)
// {
//     return b+a;
// }

int main(int argc, char *argv[])
{
	int N = atoi(argv[1]);

	// double *array_A = (double*)malloc(N * sizeof(double));
	// double *array_B = (double*)malloc(N * sizeof(double));
	// double *array_C = (double*)malloc(N * sizeof(double));

    // double *array_A = (double*)_mm_malloc(N * sizeof(double),sizeof(double));
    // double *array_B = (double*)_mm_malloc(N * sizeof(double),sizeof(double));
    // double *array_C = (double*)_mm_malloc(N * sizeof(double),sizeof(double));
// 
    double *array_A = (double*)_mm_malloc(N * sizeof(double),64);
    double *array_B = (double*)_mm_malloc(N * sizeof(double),64);
    double *array_C = (double*)_mm_malloc(N * sizeof(double),64);

	// double **array_A_a = (double**)malloc((N*N) * sizeof(double*));
	// double **array_B_a = (double**)malloc((N*N) * sizeof(double*));
	// double **array_C_a = (double**)malloc((N*N) * sizeof(double*));

	for(int i=0; i<N; i++)
    {
    	array_A[i] = 0.5;
    	// array_A_a[i] = &array_A[i];
    	array_B[i] = 0.5;
    	// array_B_a[i] = &array_B[i];
    	array_C[i] = 0.0;
    	// array_C_a[i] = &array_C[i];
    }

    // printf("%d\n", sizeof(double));

    // for(int i=0; i<N; i++)
    // {
    //     printf("%p\n", &array_A[i]);
    //     printf("%p\n", &array_B[i]);
    //     printf("%p\n", &array_C[i]);
    //     printf("----\n");
    // }


    // double sum = 0;

    double start = omp_get_wtime();
    
	// // #pragma omp simd reduction(+:sum) aligned(array_A_a:8) aligned(array_B_a:8) 
 //    // #pragma omp simd safelen(10) reduction(+:sum) schedule(simd:static)
 //    // #pragma omp simd simdlen(4) collapse(3)
 //    // #pragma omp parallel for schedule(static) reduction(+:array_C[:N])
 //    // #pragma omp parallel for schedule(ompSched,chunkSize)
 //                    // array_C[i] = array_C[i] + array_A[i] + array_B[i];
 //                    // array_C[k] += method(array_A[k], array_B[k]);
 //    // #pragma omp parallel for collapse(3) reduction(+:sum)
 //    // #pragma omp simd collapse(3)
    
    // __assume_aligned(array_A, sizeof(double));
    // __assume_aligned(array_B, sizeof(double));
    // __assume_aligned(array_C, sizeof(double));
    // #pragma omp simd simdlen(8)
    // #pragma omp simd simdlen(8) aligned(array_A:8) aligned(array_B:8) aligned(array_C:8) collapse(3)
    // #pragma omp simd 
            // #pragma clang loop vectorize(enable)

    // #pragma omp simd simdlen(16) aligned(array_A:8) aligned(array_B:8) aligned(array_C:8)
    
    // #pragma omp parallel for num_threads(8) schedule(static,1) reduction(+:array_C[:N])
    for(int j=0; j<N; j++)
    {  
        // double itrStart = omp_get_wtime();
     
    // //     __assume_aligned(array_A, sizeof(double));
    // // __assume_aligned(array_B, sizeof(double));
    // // __assume_aligned(array_C, sizeof(double));
        
    //     // #pragma omp simd simdlen(16) aligned(array_A:8) aligned(array_B:8) aligned(array_C:8)
    //     // #pragma omp simd
        for(int p=0; p<N; p++)
        {
            // #pragma omp simd simdlen(8) aligned(array_A:64) aligned(array_B:64) aligned(array_C:64)
            // #pragma omp parallel for
            for(int k=0; k<N; k++)
            {
                array_C[k] += array_A[k] + array_B[k];
            // array_C[k+1] += array_A[k+1] + array_B[k+1];
            }
        }
        // double itrEnd = omp_get_wtime();
        // printf("%f,", itrEnd-itrStart);
    }

	// // gettimeofday(&t1, 0);
	double end = omp_get_wtime();
 //    printf("%f\n", array_C[0]);

    double sum = 0;
    for(int i=0; i<N; i++)
    {
        sum = array_C[i] + sum;
    }
	// // double elapsed = (t1.tv_sec-t0.tv_sec) * 1.0f + (t1.tv_usec - t0.tv_usec) / 1000000.0f;
	double elapsed = end -start;
	printf("%f\n", elapsed);
    printf("%f\n", sum);

	return 0;
}