import timeit
from ctypes import c_int

import numpy as np
import numpy.ctypeslib as npct

from matrix_ import get_matrix_experiment_args


def naive_matmul(a, b, c, cm):
    array_2d_double_p = npct.ndpointer(
        dtype=np.double,
        ndim=2,
        flags='C_CONTIGUOUS'
    )
    lib_matrix_funcs = npct.load_library('libmatrix_funcs_with_links', '../c')
    lib_matrix_funcs.naive_matmul.argtypes = [
        array_2d_double_p,
        array_2d_double_p,
        array_2d_double_p,
        c_int,
        c_int,
        c_int,
        c_int
    ]
    M = a.shape[0]
    N = b.shape[1]
    K = a.shape[1]
    lib_matrix_funcs.naive_matmul(a, b, c, M, N, K, cm)


def main():
    args = get_matrix_experiment_args()

    
    a = np.random.rand(args.M, args.K)
    b = np.random.rand(args.K, args.N)
    c = np.zeros([args.M, args.N])

    t = timeit.timeit(
        stmt="naive_matmul(a, b, c, cm)",
        number=args.number_of_repeats,
        globals={
            "naive_matmul": naive_matmul,
            "a": a,
            "b": b,
            "c": c,
            "cm": args.make_col_major_in_b,
        }
    )
    print(t / args.number_of_repeats)


if __name__ == '__main__':
    main()
            
