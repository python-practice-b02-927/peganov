#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <cblas.h>


int
naive_matmul(
	const double *a, 
	const double *b, 
	double *c, 
	const int M, 
	const int N, 
	const int K,
	const int make_b_col_major)
{
	int i, j, k;
	double *bb;
	if (make_b_col_major > 0){
		bb = (double *)malloc(K * N * sizeof(double));
		for(i = 0; i < K; i++){
			for(j = 0; j < N; j++){
				bb[j*K + i] = b[i*N + j];
			}
		}
	}
	for(i = 0; i < M; i++){
		for(j = 0; j < N; j++){
			for(k = 0; k < K; k++){
				if (make_b_col_major > 0)
					c[i*N+j] += a[i*K+k] * bb[j*K+k];
				else
					c[i*N+j] += a[i*K+k] * b[k*N+j];
			}
		}
	}
	if (make_b_col_major > 0)
		free(bb);
	return 0;
}



int
init_random_matrix(double *a, const int M, const int N)
{
	int i, j;
	for(i = 0; i < M; i++){
		for(j = 0; j < N; j++){
			a[i*N + j] = (double)(rand() - RAND_MAX / 2) 
				/ (RAND_MAX / 2);
		}
	}
	return 0;
}


int
print_matrix(const double *a, const int M, const int N)
{
	int i, j;
	for(i = 0; i < M; i++){
		for(j = 0; j < N; j++){
			printf("%f ", a[i*N+j]);
		}
		printf("\n");
	}
	return 0;
}


int
zero_matrix(double *a, const int M, const int N)
{
	int i, j;
	for(i = 0; i < M; i++){
		for(j = 0; j < N; j++){
			a[i*N + j] = 0;
		}
	}
	return 0;
}


double
measure_mm_time(
	const int n,
	const char *method, 
	double *a, 
	double *b, 
	double *c,
	const int M,
	const int N,
	const int K)
{
	clock_t total = 0, t;
	int i;
	for(i = 0; i < n; i++){
		init_random_matrix(a, M, K);
		init_random_matrix(b, K, N);
		if (strcmp(method, "naive") == 0){
			t = clock();
			naive_matmul(a, b, c, M, N, K, 0);
			total += clock() - t;
		} else if (strcmp(method, "cblas") == 0){
			t = clock();
 			cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
 				M, N, K, 1, a, K, b, N, 1, c, N);
 			total += clock() - t;
		} else
			return -1;
		zero_matrix(c, M, N);
	}
	return (double)total / CLOCKS_PER_SEC / n;
}
