import timeit

import numpy as np

from matrix_ import get_matrix_experiment_args
from naive import naive


def main():
    args = get_matrix_experiment_args()
    a = np.random.rand(args.M, args.K)
    b = np.random.rand(args.K, args.N)
    c = np.zeros([args.M, args.N])
    t = timeit.timeit(
        stmt="naive_matmul(a, b, c, M, N, K, int(cm))",
        number=args.number_of_repeats,
        globals={
            "naive_matmul": naive.naive_matmul,
            "a": a,
            "b": b,
            "c": c,
            "M": args.M,
            "N": args.N,
            "K": args.K,
            "cm": args.make_col_major_in_b,
        }
    )
    print(t / args.number_of_repeats)


if __name__ == "__main__":
    main()

