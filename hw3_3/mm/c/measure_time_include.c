#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "matrix_funcs.h"



int
main(int argc, char *argv[])
{
	double naive_time, cblas_time;
	int n_naive, n_blas;
	double *a, *b, *c;
	int  M, N, K;

	srand(time(NULL));

	n_naive = atoi(argv[1]);
	n_blas = atoi(argv[2]);
	M = atoi(argv[3]);
	N = atoi(argv[4]);
	K = atoi(argv[5]);

	a = (double *)calloc(M * K, sizeof(double));
	b = (double *)calloc(K * N, sizeof(double));
	c = (double *)calloc(M * N, sizeof(double));

	naive_time = measure_mm_time(n_naive, "naive", a, b, c, M, N, K);
	if (naive_time < 0)
		return -1;
	cblas_time = measure_mm_time(n_blas, "cblas", a, b, c, M, N, K);
	if (cblas_time < 0)
		return -1;
	free(a);
	free(b);
	free(c);
	printf("naive mm time:\t%f\n", naive_time);
	printf("cblas mm time:\t%f\n", cblas_time);
	return 0;
}
