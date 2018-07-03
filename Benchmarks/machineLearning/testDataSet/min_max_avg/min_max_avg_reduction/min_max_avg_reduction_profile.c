#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
	if (argc != 2)
	{
		printf("Usage: %s <n>\n", argv[0]);
		return 0;
	}

	int n = atoi(argv[1]);

	double* x = (double*)malloc(sizeof(double) * n);
	double* y = (double*)malloc(sizeof(double) * n);

	double idrandmax = 1.0 / RAND_MAX;
	double a = idrandmax * rand();
	for (int i = 0; i < n; i++)
	{
		x[i] = idrandmax * rand();
		y[i] = idrandmax * rand();
	}

double avg = 0.0,min = y[0], max = y[0];


  for (int j = 0; j < n; j++)
  {
		for (int i = 0; i < n; i++)
    {
			y[i] += a * x[i];
			avg += y[i];

    }
}


	for (int i = 0; i < n; i++)
	{
    avg += y[i];
		if (y[i] > max) max = y[i];
		if (y[i] < min) min = y[i];
	}


	free(x);
	free(y);

	return 0;
}
