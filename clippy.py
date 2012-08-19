"""
CLiPPY : simple python bindings to COIN-OR's CLP library
"""

import numpy
from numpy.ctypeslib import ndpointer
import ctypes

_OPTIMISATION_MODE_PRIMAL = 0
_OPTIMISATION_MODE_DUAL = 1

OPTIMISATION_MODES = {
    'primal' : _OPTIMISATION_MODE_PRIMAL,
    'dual' : _OPTIMISATION_MODE_DUAL,
}

class clp_result_t(ctypes.Structure):
    _fields_ = [
        ('proven_optimal', ctypes.c_int),
        ('proven_primal_infeasible', ctypes.c_int),
        ('proven_dual_infeasible', ctypes.c_int),
        ('abandoned', ctypes.c_int),
    ]


def _make_clp_solve(library_path = 'src/libclpsolve.so'):
    lib = ctypes.CDLL(library_path)

    _clp_solve = lib.clp_solve
    _clp_solve.argtypes = [
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ndpointer(dtype = numpy.int32),
        ndpointer(dtype = numpy.int32),
        ndpointer(dtype = numpy.float64),
        ndpointer(dtype = numpy.float64),
        ndpointer(dtype = numpy.float64),
        ndpointer(dtype = numpy.float64),
        ndpointer(dtype = numpy.float64),
        ndpointer(dtype = numpy.float64),
        ctypes.c_int,
        ndpointer(dtype = numpy.float64),
    ]
    _clp_solve.restype = clp_result_t

    def clp_solve(((m, n), (a_rows, a_cols, a_coeffs)), c, b_lo, b_up, x_lo,
            x_up, optimisation_mode='primal'):
        """
        Solve given LP via CLP

        arguments:
            (m, n) : shape of sparse matrix A
            (a_rows, a_cols, a_coeffs) : COO-rdinate data for sparse matrix A
            c : cost vector, length n
            b_lo, b_up : lower and upper bounds on Ax, length m
            x_lo, x_up : lower and upper bounds on x, length n
            optimisation_mode : optional, either 'primal' or 'dual'
        return value:
            {
                'proven_optimal' : bool
                'proven_primal_infeasible' : bool
                'proven_dual_infeasible' : bool
                'abandoned' : bool
                'x' : numpy array of length n containing solution
            }
        """

        a_rows = numpy.asarray(a_rows, dtype=numpy.int32)
        a_cols = numpy.asarray(a_cols, dtype=numpy.int32)
        a_coeffs = numpy.asarray(a_coeffs, dtype=numpy.float64)
        c = numpy.asarray(c, dtype=numpy.float64)
        b_lo = numpy.asarray(b_lo, dtype=numpy.float64)
        b_up = numpy.asarray(b_up, dtype=numpy.float64)
        x_lo = numpy.asarray(x_lo, dtype=numpy.float64)
        x_up = numpy.asarray(x_up, dtype=numpy.float64)

        n_entries = a_rows.shape[0]
        assert n_entries == a_cols.shape[0] == a_coeffs.shape[0]
        assert c.shape[0] == x_lo.shape[0] == x_up.shape[0] == n
        assert b_lo.shape[0] == b_up.shape[0] == m

        x = numpy.zeros((n, ), dtype = numpy.float64)

        _result = _clp_solve(
            m,
            n,
            n_entries,
            a_rows,
            a_cols,
            a_coeffs,
            c,
            b_lo,
            b_up,
            x_lo,
            x_up,
            OPTIMISATION_MODES[optimisation_mode],
            x,
        )

        result = {
            'proven_optimal' : bool(_result.proven_optimal),
            'proven_primal_infeasible' : bool(_result.proven_primal_infeasible),
            'proven_dual_infeasible' : bool(_result.proven_dual_infeasible),
            'abandoned' : bool(_result.abandoned),
            'x' : x,
        }
        
        return result

    return clp_solve

clp_solve = _make_clp_solve()

