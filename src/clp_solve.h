#ifndef CLP_SOLVE_H
#define CLP_SOLVE_H

#include <coin/ClpSimplex.hpp>
#include <coin/CoinPackedMatrix.hpp>
#include <assert.h>

#ifdef __cplusplus
extern "C" {
#endif

#define USE_PRIMAL 0
#define USE_DUAL 1
#define USE_BARRIER 2

typedef struct {
    int proven_optimal;
    int proven_primal_infeasible;
    int proven_dual_infeasible;
    int abandoned;
} clp_result_t;

clp_result_t clp_solve(int n_rows, int n_cols, int n_entries,
        const int *row_indices, const int *col_indices,
        const double *coeffs, const double *vec_c,
        const double *vec_b_lo, const double *vec_b_up,
        const double *vec_x_lo, const double *vec_x_up,
        int optimisation_mode, double *vec_x_soln);

#ifdef __cplusplus
}
#endif

#endif /* CLP_SOLVE_H */
