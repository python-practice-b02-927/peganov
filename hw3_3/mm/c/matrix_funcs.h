int naive_matmul(
	const double *a, 
	const double *b, 
	double *c, 
	const int M, 
	const int N, 
	const int K,
	const int make_b_col_major);


int init_random_matrix(double *a, const int M, const int N);


int print_matrix(const double *a, const int M, const int N);


int zero_matrix(double *a, const int M, const int N);


double
measure_mm_time(
	const int n,
	const char *method, 
	double *a, 
	double *b, 
	double *c,
	const int M,
	const int N,
	const int K);
