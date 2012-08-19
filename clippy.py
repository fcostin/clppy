"""
CLiPPY : simple python bindings to COIN-OR's CLP library
"""

import numpy
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
        ('proven_dual_infeasibile', ctypes.c_int),
        ('abandoned', ctypes.c_int),
    ]

class coo_matrix_t(ctypes.Structure):
    _fields_ = [
        ('n_rows', ctypes.c_int),
        ('n_cols', ctypes.c_int),
        ('n_entries', ctypes.c_int),
        ('row_indices', ctypes.POINTER(ctypes.c_int)),
        ('col_indices', ctypes.POINTER(ctypes.c_int)),
        ('coeffs', ctypes.POINTER(ctypes.c_double)),
    ]

class clp_params_t(ctypes.Structure):
    _fields_ = [
        ('optimisation_mode', ctypes.c_int),
    ]

def _pointer_to_int(a):
    return numpy.asarray(a).ctypes.data_as(ctypes.POINTER(ctypes.c_int))

def _pointer_to_double(a):
    return numpy.asarray(a).ctypes.data_as(ctypes.POINTER(ctypes.c_double))

def _make_clp_solve(library_path = 'src/libclpsolve.so'):
    lib = ctypes.CDLL(library_path)

    _clp_solve = lib.clp_solve
    _clp_solve.argtypes = [
        ctypes.POINTER(coo_matrix_t),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(clp_params_t),
        ctypes.POINTER(ctypes.c_double),
    ]
    _clp_solve.restype = clp_result_t

    def clp_solve((m, n), (a_rows, a_cols, a_coeffs), c, b_lo, b_up, x_lo,
            x_up, optimisation_mode='primal'):
        """
        Solve given LP via CLP

        arguments:
            (m, n) : shape of matrix A
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

        a_rows = numpy.asarray(a_rows, dtype=numpy.int_)
        a_cols = numpy.asarray(a_cols, dtype=numpy.int_)
        a_coeffs = numpy.asarray(a_coeffs, dtype=numpy.double_)
        c = numpy.asarray(c, dtype=numpy.double_)
        b_lo = numpy.asarray(b_lo, dtype=numpy.double_)
        b_up = numpy.asarray(b_up, dtype=numpy.double_)
        x_lo = numpy.asarray(x_lo, dtype=numpy.double_)
        x_up = numpy.asarray(x_up, dtype=numpy.double_)

        n_entries = a_rows.shape[0]
        assert n_entries == a_cols.shape[0] == a_coeffs.shape[0]
        assert c.shape[0] == x_lo.shape[0] == x_up.shape[0] == n
        assert b_lo.shape[0] == b_up.shape[0] == m


        x = numpy.zeros((n, ), dtype = numpy.double_)

        a_matrix = coo_matrix_t(
            m, n, n_entries, _pointer_to_int(a_rows), _pointer_to_int(a_cols),
            _pointer_to_double(a_coeffs))

        params = clp_params_t(OPTIMISATION_MODES[optimisation_mode])

        _result = _clp_solve(
            mat_a = ctypes.POINTER(a_matrix),
            vec_c = _pointer_to_double(c),
            vec_b_lo = _pointer_to_double(b_lo),
            vec_b_hi = _pointer_to_double(b_hi),
            vec_x_lo = _pointer_to_double(x_lo),
            vec_x_hi = _pointer_to_double(x_hi),
            params = ctypes.POINTER(params),
            vec_x_soln = _pointer_to_double(x),
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

