#include <stdio.h>
#include <omp.h>

int main()
{

    for (int i = 4; i < 100; i++)
    {
        for (int i = 3; i < 100; i++)
        {
            printf("loop3%d\n",omp_get_num_threads());
        }
        printf("loop4%d\n",omp_get_num_threads());
    }


    omp_set_nested(1);
    int dummyVariable = 0;
    #pragma omp parallel  proc_bind(    master)  num_threads(5) reduction(+:dummyVariable) default(shared) if(1>0)
    {
        #pragma omp for schedule(static,1) nowait ordered(8)
        for (int i = 1; i < 100; i++)
        {
            printf("loop1%d\n",omp_get_num_threads());
        }
    }

    #pragma omp parallel for schedule(static) 
    for (int i = 2; i < 100; i++)
    {
        printf("loop2%d\n",omp_get_num_threads());
    }

    return(0);
}

