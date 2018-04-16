#include <stdio.h>
#include <omp.h>

void testMethod(){
    printf("in method");
}

int main()
{
    omp_set_nested(1);
    testMethod();
    #pragma omp parallel  proc_bind(\
    master)     num_threads    (    5    )


        #pragma omp for schedule          (      static           ,          1           )

        for (int i = 0; i < 100; i++)/*sdsdsdsdsd
        sdssds
        sds
        */
        {
            printf("%d\n",omp_get_num_threads());
    //        for (int i = 0; i < 100; i++)
    //        {
    //            printf("%d\n",omp_get_num_threads());
        //        omp_set_num_threads(10);
        //        #pragma omp parallel for
        //        for(int i = 0; i < 4; i++)
        //        {
        //            printf("%d\n",omp_get_num_threads());
        //        }
   /*sdsdsdsdsd
        sdssds
        sds
        */
        }


    #pragma omp parallel          for  //sdsdsd\sdsdsd
    for (int i = 0; i < 100; i++)/*sdsdsdsdsd
        sdssds
        sds
        */
        {
            printf("%d\n",omp_get_num_threads());
    //        for (int i = 0; i < 100; i++)
    //        {
    //            printf("%d\n",omp_get_num_threads());
        //        omp_set_num_threads(10);
        //        #pragma omp parallel for
        //        for(int i = 0; i < 4; i++)
        //        {
        //            printf("%d\n",omp_get_num_threads());
        //        }
   /*sdsdsdsdsd
        sdssds
        sds
        */
        }
    return(0);
}

