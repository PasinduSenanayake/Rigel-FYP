#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
/*
 * Author: Soeren Gebbert
 * (c) 2013 Soeren Gebbert and the GRASS Development Team
 * Licensed as GPL >=2. See the COPYING file which comes with GRASS for details.
 *
 * http://thread.gmane.org/gmane.comp.gis.grass.user/47627/focus=47667
 */

/* #define DEBUG 1 */

/* Prototypes for gathering and average computation */
static int gather_values(double **input, double *buff, int nrows,
        int ncols, int mw_size, int col, int row, int dist);

static double average(double *values, int size);

int main(int argc, char **argv)
{
    int nrows, ncols, mw_size, size, dist;
    double **input = NULL, **output = NULL;
    int i, j;

    /* Check and parse the input parameter */
    if(argc != 4)
    {

        fprintf(stderr, "Warning!\n");
        fprintf(stderr, "Please specifiy the number of rows and columns and the "
                "\nsize of the moving window (must be an odd number)\n");
        fprintf(stderr, "\nUsage: neighbor 5000 5000 51\n");
        fprintf(stderr, "\nUsing default values: rows = 5000, cols = 5000, moving window = 51\n");
        nrows = 5000;
        ncols = 5000;
        mw_size = 51;
    }
    else
    {

        sscanf(argv[1], "%d", &nrows);
        sscanf(argv[2], "%d", &ncols);
        sscanf(argv[3], "%d", &mw_size);

        if(mw_size%2 == 0) {
            fprintf(stderr,"The size of the moving window must be odd");
            return -1;
        }
    }

    size = mw_size * mw_size;
    dist = mw_size / 2;

    /* Allocate input and output */
    input = (double**)calloc(nrows, sizeof(double*));
    output= (double**)calloc(nrows, sizeof(double*));

    if(input == NULL || output == NULL)
    {
        fprintf(stderr, "Unable to allocate arrays");
        return -1;
    }

    for(i = 0; i < nrows; i++)
    {
        input[i] = (double*)calloc(ncols, sizeof(double));
        output[i]= (double*)calloc(ncols, sizeof(double));

        if(input[i] == NULL || output[i] == NULL)
        {
            fprintf(stderr, "Unable to allocate arrays");
            return -1;
        }

#ifdef DEBUG
        for(j = 0; j < ncols; j++)
            input[i][j] = i + j;
#endif
    }
    double *buff = NULL;
    buff = (double*)calloc(size, sizeof(double));
double startTime = omp_get_wtime();
#pragma omp parallel for schedule(dynamic) private(i, j)
    for(i = 0; i < nrows; i++)
    {
        for(j = 0; j < ncols; j++)
        {
        int num = gather_values(input, buff, nrows, ncols, mw_size, i, j, dist);

        output[i][j] = average(buff, num);


        }
    }
      free(buff);
  printf("Runtime Dynamic CoreTest: %f\n",omp_get_wtime()-startTime );

#ifdef DEBUG
    printf("\nInput\n");
    for(i = 0; i < nrows; i++)
    {
        for(j = 0; j < ncols; j++)
        {
            printf("%.2f ", input[i][j]);
        }
        printf("\n");
    }

    printf("\nOutput\n");
    for(i = 0; i < nrows; i++)
    {
        for(j = 0; j < ncols; j++)
        {
            printf("%.2f ", output[i][j]);
        }
        printf("\n");
    }
#endif

    return 0;
}

int gather_values(double **input, double *buff, int nrows,
        int ncols, int mw_size, int col, int row, int dist)
{
    int i, j, k;

    int start_row = row - dist;
    int start_col = col - dist;
    int end_row = start_row + mw_size;
    int end_col = start_col + mw_size;

    if(start_row < 0)
        start_row = 0;

    if(start_col < 0)
        start_col = 0;

    if(end_row > nrows)
        end_row = nrows;

    if(end_col > ncols)
        end_col = ncols;

    k = 0;

    for(i = start_row; i < end_row; i++)
    {
        for(j = start_col; j < end_col; j++)
        {
            buff[k] = input[i][j];
            k++;
        }
    }

    return k;
}

double average(double *values, int size)
{
    int i;
    double a = 0.0;
    for(i = 0; i < size; i++)
        a += values[i];

    a = a / (double)size;
    return a;
}
