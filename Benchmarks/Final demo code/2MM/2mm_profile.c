#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include <stdbool.h>


# define NI 1024
# define NJ 1024
# define NK 1024
# define NL 1024

# define NIV 512
# define NJV 512
# define NKV 512
# define NLV 512


#define NUM 350000
#define NP 50000

int nums[NUM];
int primes[NP];
int np = 0;

typedef float DATA_TYPE;

float F[NLV][NLV],G[NLV][NLV],H[NLV][NLV],I[NLV],J[NLV],K[NLV],L[NLV];

struct triplet
{
	int a;
	int b;
	int c;
};


//----> AdditionalCodeHook


int dummy(float[NLV][NLV], float[NLV][NLV], float[NLV][NLV], float[NLV], float[NLV], float[NLV], float[NLV]);

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

   #pragma omp parallel for
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

void kernel_vec()
{
  #pragma omp parallel for num_threads(1)
  for (int nl = 0; nl < 100*(20000/256); nl++)
  {
    for (int i = 0; i < NLV; i++)
    {
      for (int j = 0; j < NLV; j++)
      {
        F[j][i] = F[j][i] + G[j][i] * H[j][i];
      }
      I[i] = J[i] + K[i] * L[i];
    }
    dummy(F,G,H,I,J,K,L);
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

	kernel_vec();

  int *set1=malloc(sizeof(int)*10);
  int *set2=malloc(sizeof(int)*10);
  int *set3=malloc(sizeof(int)*10);

  init();
  genPrimes();

    #pragma omp parallel for schedule(static)
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
