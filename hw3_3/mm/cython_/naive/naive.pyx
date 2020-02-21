cimport numpy

import numpy as np


def naive_matmul(
        const double[:, :] a, 
        const double[:, :] b, 
        double[:, :] c,
        const int M,
        const int N,
        const int K,
        const int make_col_major_in_b
):
    cdef int i, j, k
    cdef double[:, :] bb = np.zeros([N, K])
    cdef double s
    for i in range(K):
        for j in range(N):
            bb[j, i] = b[i, j]
    for i in range(M):
        for j in range(N):
            s = 0
            for k in range(K):
                if make_col_major_in_b:
                    s += bb[j, k] * a[i, k]
                else:
                    s += b[k, j]
            c[i, j] = s
    return 0

