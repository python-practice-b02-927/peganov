import timeit

import numpy as np

from matrix_ import get_matrix_experiment_args
from cblas import cblas_matmul


def main():
    args = get_matrix_experiment_args()
    a = np.random.rand(args.M, args.K)
    b = np.random.rand(args.K, args.N)
    t = timeit.timeit(
        stmt="c = cblas_matmul(a, b)",
        number=args.number_of_repeats,
        globals={
            "cblas_matmul": cblas_matmul.cblas_matmul,
            "a": a,
            "b": b,
        }
    )
    print(t / args.number_of_repeats)


if __name__ == "__main__":
    main()

