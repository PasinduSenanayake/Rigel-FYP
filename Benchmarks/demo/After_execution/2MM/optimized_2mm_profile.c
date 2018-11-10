#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include <stdbool.h>

# define NI 64
# define NJ 64
# define NK 64
# define NL 64

#define NUM 350000
#define NP 50000

int nums[NUM];
int primes[NP];
int np = 0;

typedef float DATA_TYPE;

struct triplet
{
	int a;
	int b;
	int c;
};


//----> AdditionalCodeHook

void init_array(DATA_TYPE* A, DATA_TYPE* B)
{
  int i, j;

  for (i = 0; i < NI; i++)
    {
      for (j = 0; j < NK; j++)
	{
	  A[i*NI + j] = ((DATA_TYPE) i*j) / NI;
	}
    }

  for (i = 0; i < NK; i++)
    {
      for (j = 0; j < NJ; j++)
	{
	  B[i*NK + j] = ((DATA_TYPE) i*(j+1)) / NJ;
	}
    }

}


void mm2_OMP(DATA_TYPE* A, DATA_TYPE* B,DATA_TYPE* D)
{

   #pragma omp target data map(to:A[0:64]) map(tofrom:D[0:64]) map(to:B[0:64])
#pragma omp target teams thread_limit(256)
#pragma omp distribute parallel for collapse(2) schedule(static,1) 
for (int i = 0; i < NI; i++)
     {
       for (int j = 0; j < NJ; j++)
	 {
	   D[i*NJ + j] = 0.0;
	   for (int k = 0; k < NK; ++k)
	     {
	       D[i*NJ + j] += A[i*NK + k] * B[k*NJ + j];
	     }
	 }
     }



}

void printNums()
{
	for(int i=0;i<NUM;i++)
	{
		if(nums[i]==0)
		{
			printf("%d\n",i);
		}
	}
}

void init()
{
	for(int i =0; i<NUM;i++)
	{
		nums[i]=0;
	}
}
void genPrimes()
{
	nums[0]=1;
	nums[1]=1;
	nums[2]=0;
	{

		for(int i = 2;i<NUM;i++)
		{
			int itrn=NUM/i;
			if(nums[i]==0)
			{
				if(i>1000)
				{
					primes[np]=i;
					np++;
				}
				for(int j=2;j<=itrn;j++)
				{
					nums[i*j]=1;
				}
			}
		}

	}
}


int main(int argc, char** argv)
{

  DATA_TYPE* A;
  DATA_TYPE* B;
  DATA_TYPE* D;


  A = (DATA_TYPE*)malloc(NI*NK*sizeof(DATA_TYPE));
  B = (DATA_TYPE*)malloc(NK*NJ*sizeof(DATA_TYPE));
  D = (DATA_TYPE*)malloc(NJ*NL*sizeof(DATA_TYPE));

  init_array(A, B);

  mm2_OMP(A, B, D);

  free(A);
  free(B);
  free(D);

  int *set1=malloc(sizeof(int)*10);
  int *set2=malloc(sizeof(int)*10);
  int *set3=malloc(sizeof(int)*10);

  init();
  genPrimes();

    #pragma omp parallel for schedule(guided)
    for(int i=0;i<np-2;i++)
    {

			for(int i=0;i<10;i++){
				set1[i]=0;
			}
			int n = primes[i];
			while(n)
			{
				int i = n%10;
					if(i>=0&& i<10){
							set1[i]++;
						}
					n/=10;
			 }
       for(int j=i+1;j<np;j++)
      	{
        int diff = primes[j]-primes[i];
        int p2 = primes[j]+diff;
        if(p2<NUM && nums[p2]==0)
        {
					for(int i=0;i<10;i++){
						set2[i]=0;
					}
					int n = primes[j];
					while(n)
					{
						int i = n%10;
						if(i>=0&& i<10){
							set2[i]++;
						}
						n/=10;
					}

					bool compTest = true;
					for(int i=0;i<10;i++)
					{
						if(set1[i]!=set2[i]){
							if(compTest){
								compTest = false;
								}
							}
					}
          if(compTest)
          {
						for(int i=0;i<10;i++){
							set3[i]=0;
						}

						int n = p2;
						while(n)
						{
							int i = n%10;
							if(i>=0&& i<10){
								set3[i]++;
							}
							n/=10;
						}
          }
      		}
      	}
    }
  return 0;
}
