clp.py
======

A simple python interface to COIN-OR's `clp` solver.

### Files

These files define `libclpsolve.so`, a dynamic library with a simple interface to
`clp`, using C linkage:

    src/clp_solve.h
    src/clp_solve.cpp
    src/Makefile

`clp.py` is a wrapper module that links to `libcplsolve.so` via `ctypes` and defines a slightly friendlier interface:

    clp.py

Here is the `clp_solve` function provided by `clp.py`:

    def clp_solve(((m, n), (a_rows, a_cols, a_coeffs)), c, b_lo, b_up, x_lo,
            x_up, optimisation_mode='barrier'):
        """
        Solve given LP via CLP

        arguments:
            (m, n) : shape of sparse matrix A
            (a_rows, a_cols, a_coeffs) : COO-rdinate data for sparse matrix A
            c : cost vector, length n
            b_lo, b_up : lower and upper bounds on Ax, length m
            x_lo, x_up : lower and upper bounds on x, length n
            optimisation_mode : optional, either 'primal', 'dual' or 'barrier'
        return value:
            {
                'proven_optimal' : bool
                'proven_primal_infeasible' : bool
                'proven_dual_infeasible' : bool
                'abandoned' : bool
                'x' : numpy array of length n containing solution
            }
        """


### Portability

Assumes `sizeof(int)` is 4 and `sizeof(double)` is 8. Will need a bit of modification if this is not the case. Tested on 64-bit Debian only.

### Dependencies

*   [python][]
*   [ctypes][]
*   [numpy][]
*   [clp][]

### License

BSD. See `LICENSE.txt`


[numpy]:    http://numpy.scipy.org/
[clp]:      http://www.coin-or.org/projects/Clp.xml
[python]:   http://python.org/
[ctypes]:   http://docs.python.org/library/ctypes

