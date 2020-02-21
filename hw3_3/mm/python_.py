import timeit

from matrix_ import *


def main():
    args = get_matrix_experiment_args()
    a = init_random_matrix(args.M, args.K)
    b = init_random_matrix(args.K, args.N)
    if args.preallocate_c:
        c = [[0. for _ in range(args.N)] for _ in range(args.M)]
    else:
        c = None
    t = timeit.timeit(
        stmt="c1 = matmul(a, b, c, cm)",
        number=args.number_of_repeats,
        globals={
            "matmul": matmul, 
            "a": a, 
            "b": b,
            "c": c, 
            "cm": args.make_col_major_in_b
        },
    )
    print(t / args.number_of_repeats)
    
    a = [[1, 2, 3], [4, 5, 6]]
    b = [[1, 2], [3, 4], [5, 6]]
    c = [[0., 0.], [0., 0.]]
    print_2d_nested_list(matmul(a, b, None, False))
    matmul(a, b, c, False)
    print_2d_nested_list(c)


if __name__ == '__main__':
     main()

