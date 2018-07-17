//
// main.c: Demo of multi-target mulit-source OpenMP offload
//         Sources are main.c, vmul.c, and vsum.c
//         offload targets are nvptx64 and amdgcn
//

#include <stdio.h>
#include <omp.h>


int main(int argc, char* argv[]){
  int N = atoi(argv[1]);
   int a[N],b[N],c[N];

   for(int i=0;i<N;i++) {
      a[i] = i;
      b[i] = i+1;
   }
double startTime = omp_get_wtime();
#pragma omp target teams map(to: a[0:N],b[0:N]) map(from:c[0:N])
#pragma omp distribute parallel for

//#pragma omp parallel for
   for(int j=0;j<N;j++) {
    for(int i=0;i<N;i++) {
       c[i]=a[i]*b[i]*j;
    }
 }

printf("%f\n",omp_get_wtime()-startTime );

   return 0;
}
