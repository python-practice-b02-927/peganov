import argparse
import random

from numba import jit


def get_matrix_experiment_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--number_of_repeats",
        "-n",
        help="Number of times multiplication is repeated."
             " Default is 1",
        type=int,
        default=1,
    )
    parser.add_argument(
        "-M",
        help="Number of rows in the first matrix. "
             "Default is 1000.",
        type=int,
        default=1000,
    )
    parser.add_argument(
        "-N",
        help="Number of columns in the second matrix. "
             "Default is 2000",
        type=int,
        default=2000,
    )
    parser.add_argument(
        "-K",
        help="Number of columns in the first matrix and "
             "number of rows in the second matrix. "
             "Default is 1500.",
        type=int,
        default=1500,
    )
    parser.add_argument(
        "--preallocate_c",
        "-a",
        help="If option is specified space for matrix"
             " is preallocated outside multiplication"
             " function",
        action="store_true",
    )
    parser.add_argument(
        "--make_col_major_in_b",
        "-c",
        help="If option is provided matrix `b` is "
             "restructured to make columns major dimension.",
        action="store_true",
    )
    args = parser.parse_args()
    return args


def init_random_matrix(M, N):
    a = [[random.uniform(-1, 1) for _ in range(N)] for _ in range(M)]
    return a


def print_2d_nested_list(nested_list):
    for list_ in nested_list:
        print(list_)


def matmul(a, b, c, make_col_major_in_b):
    bb = None
    if make_col_major_in_b:
        bb = []
        for j in range(len(b[0])):
            row = []
            for i in range(len(b)):
                row.append(b[i][j])
            bb.append(row)
    if c is None:
        c_preallocated = False
        c = []
        for i in range(len(a)):
            row = []
            for j in range(len(b[0])):
                s = 0
                for k in range(len(b)):
                    if make_col_major_in_b:
                        s += a[i][k] * bb[j][k]
                    else:
                        s += a[i][k] * b[k][j]
                row.append(s)
            c.append(row)
    else:
        c_preallocated = True
        for i in range(len(a)):
            for j in range(len(b[0])):
                s = 0
                for k in range(len(b)):
                    if make_col_major_in_b:
                        s += a[i][k] * bb[j][k]
                    else:
                        s += a[i][k] * b[k][j]
                c[i][j] = s
    return None if c_preallocated else c


@jit()
def jit_matmul(a, b, c, make_col_major_in_b):
    bb = None
    if make_col_major_in_b:
        bb = []
        for j in range(len(b[0])):
            row = []
            for i in range(len(b)):
                row.append(b[i][j])
            bb.append(row)
    if c is None:
        c_preallocated = False
        c = []
        for i in range(len(a)):
            row = []
            for j in range(len(b[0])):
                s = 0
                for k in range(len(b)):
                    if make_col_major_in_b:
                        s += a[i][k] * bb[j][k]
                    else:
                        s += a[i][k] * b[k][j]
                row.append(s)
            c.append(row)
    else:
        c_preallocated = True
        for i in range(len(a)):
            for j in range(len(b[0])):
                s = 0
                for k in range(len(b)):
                    if make_col_major_in_b:
                        s += a[i][k] * bb[j][k]
                    else:
                        s += a[i][k] * b[k][j]
                c[i][j] = s
    return None if c_preallocated else c

