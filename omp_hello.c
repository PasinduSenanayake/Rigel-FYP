#include <stdio.h>
#include <omp.h>

int main()
{
    omp_set_nested(1);
    int dummyVariable = 0;
    #pragma omp parallel  proc_bind(\
    master)  num_threads(5) reduction(+:dummyVariable) default(shared) if(1>0)
    {
        #pragma omp for schedule(static,1)
        for (int i = 0; i < 100; i++)
        {
            printf("%d\n",omp_get_num_threads());
        }
    }

    #pragma omp parallel for  //this is a dummy comment
    for (int i = 0; i < 100; i++)
    {
        printf("%d\n",omp_get_num_threads());
    }
    return(0);
}

