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
    int dummyVariable = 0;/*for sdsdsdsdsds
    sd
    sd
    s for*/ {
        for (int i = 1; i < 100; i++)
        {
            printf("loop1%d\n",omp_get_num_threads());
        }
    

    for (int i = 2; i < 100; i++)
    {
        printf("loop2%d\n",omp_get_num_threads());
    }

    return(0);
}

