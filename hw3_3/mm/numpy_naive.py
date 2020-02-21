import timeit

import numpy as np

from matrix_ import *


def numpy_naive_matmul(a, b, c=None, make_col_major_in_b=True):
    bb = None
    if make_col_major_in_b:
        bb = np.zeros((b.shape[1], b.shape[0]))
        for i in range(b.shape[0]):
            for j in range(b.shape[1]):
                bb[j, i] = b[i, j]
    c_preallocated = c is not None
    if c is None:
        c = np.zeros([a.shape[0], b.shape[1]])
    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            s = 0
            for k in range(a.shape[1]):
                if make_col_major_in_b:
                    s += a[i, k] * bb[j, k]
                else:
                    s += a[i, k] * b[k, j]
            c[i, j] = s
    return None if c_preallocated else c


def main():
    args = get_matrix_experiment_args()
    a = np.random.rand(args.M, args.K)
    b = np.random.rand(args.K, args.N)
    if args.preallocate_c:
        c = np.zeros([args.M, args.N])
    else:
        c = None
    t = timeit.timeit(
        stmt="numpy_naive_matmul(a, b, c, cm)",
        number=args.number_of_repeats,
        globals={
            "numpy_naive_matmul": numpy_naive_matmul,
            "a": a, 
            "b": b, 
            "c": c, 
            "cm": args.make_col_major_in_b
        },
    )
    print(t / args.number_of_repeats)

    a = np.array([[1., 2., 3.], [4., 5., 6.]])
    b = np.array([[1., 2.], [3., 4.], [5., 6.]])
    c = np.zeros([2, 2])  


if __name__ == '__main__':
    main()

