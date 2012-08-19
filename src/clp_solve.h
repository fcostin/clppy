#ifndef CLP_SOLVE_H
#define CLP_SOLVE_H

#include <coin/ClpSimplex.hpp>
#include <coin/CoinPackedMatrix.hpp>
#include <assert.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int proven_optimal;
    int proven_primal_infeasible;
    int proven_dual_infeasible;
    int abandoned;
} clp_result_t;

typedef struct {
    int n_rows, n_cols;
    int n_entries;
    const int *row_indices;
    const int *col_indices;
    const double *coeffs;
} coo_matrix_t;

typedef struct {
    int optimisation_mode;
} clp_params_t;

clp_result_t clp_solve(const coo_matrix_t *mat_a, const double *vec_c,
        const double *vec_b_lo, const double *vec_b_up,
        const double *vec_x_lo, const double *vec_x_up,
        const clp_params_t *params, double *vec_x_soln);

#ifdef __cplusplus
}
#endif

#endif /* CLP_SOLVE_H */
