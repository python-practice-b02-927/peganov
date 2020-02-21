import timeit

import numpy as np

from matrix_ import *


def main():
    args = get_matrix_experiment_args()
    a = np.linspace(-1000, 1000, args.M * args.K).reshape((args.M, args.K))
    b = np.random.rand(args.K, args.N)
    t = timeit.timeit(
        stmt="c = a @ b",
        number=args.number_of_repeats,
        globals={"a": a, "b": b},
    )
    print(t / args.number_of_repeats)


if __name__ == '__main__':
    main()

