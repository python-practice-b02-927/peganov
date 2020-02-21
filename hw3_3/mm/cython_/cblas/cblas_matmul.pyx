from cython cimport view

import numpy as np

from cblas_matmul cimport *


def cblas_matmul(a, b):
    if not a.flags['C_CONTIGUOUS']:
        a = np.ascontiguousarray(a)
    if not b.flags['C_CONTIGUOUS']:
        b = np.ascontiguousarray(b)

    z = np.zeros([a.shape[0], b.shape[1]])
    if not z.flags['C_CONTIGUOUS']:
        z = np.ascontiguousarray(z)
    
    cdef double[:, ::1] aview = a
    cdef double[:, ::1] bview = b
    cdef double[:, ::1] cview = z

    cdef int M = a.shape[0]
    cdef int N = b.shape[1]
    cdef int K = a.shape[1]
    
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
        M, N, K, 1, &(aview[0][0]), K, &(bview[0][0]), N, 1, &(cview[0][0]), N)
    return np.reshape(np.asarray(cview), [M, N])

