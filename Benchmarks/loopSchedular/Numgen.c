#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main(int argc, char **argv)
{
    FILE *fp;
    fp =fopen ("randnum.txt","w");
    srand(time(NULL));
    int randomness = strtol(argv[1], NULL, 10);
    int iterations = strtol(argv[2], NULL, 10);
    for (int i = 0; i < iterations; ++i) {
        int randomNumber = (rand()%randomness);
        fprintf (fp, "%d,",randomNumber+1);
    }
    fclose(fp);
}
