import timeit
from ctypes import c_int, c_double, Union, Structure

import numpy as np
import numpy.ctypeslib as npct

from matrix_ import get_matrix_experiment_args


array_2d_double_p = npct.ndpointer(
    dtype=np.double,
    ndim=2,
    flags='C_CONTIGUOUS'
)


def cblas_matmul(a, b, c):
    lib_cblas = npct.load_library(
        'libopenblasp-r0-2ecf47d5.3.7.dev.so', 
        '/home/anton/anaconda3/lib/python3.6/site-packages/numpy/.libs',
    )
    lib_cblas.cblas_dgemm.argtypes = [
        c_int,
        c_int,
        c_int,
        c_int,
        c_int,
        c_int,
        c_double,
        array_2d_double_p,
        c_int,
        array_2d_double_p,
        c_int,
        c_double,
        array_2d_double_p,
        c_int,
    ]
    lib_cblas.cblas_dgemm.restype = None
    M = a.shape[0]
    N = b.shape[1]
    K = a.shape[1]
    lib_cblas.cblas_dgemm(
        101, 111, 111, M, N, K, c_double(1), a, K, b, N, c_double(1), c, N)


def main():
    args = get_matrix_experiment_args()
    
    a = np.random.rand(args.M, args.K)
    b = np.random.rand(args.K, args.N)
    c = np.zeros([args.M, args.N])

    t = timeit.timeit(
        stmt="cblas_matmul(a, b, c)",
        number=args.number_of_repeats,
        globals={
            "cblas_matmul": cblas_matmul,
            "a": a,
            "b": b,
            "c": c,
        }
    )
    print(t / args.number_of_repeats)


if __name__ == '__main__':
    main()

