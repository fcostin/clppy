#include "clp_solve.h"

clp_result_t clp_solve(const coo_matrix_t *mat_a, const double *vec_c,
        const double *vec_b_lo, const double *vec_b_up,
        const double *vec_x_lo, const double *vec_x_up,
        const clp_params_t *params, double *vec_x_soln) {

    // XXX TODO will Coin delete our arrays?!
    
    // build column-packed coin sparse matrix from given COO data
    CoinPackedMatrix matrix(true, mat_a->row_indices, mat_a->col_indices,
        mat_a->coeffs, (CoinBigIndex)mat_a->n_entries);
    matrix.setDimensions(mat_a->n_rows, mat_a->n_cols);

    ClpSimplex model;
    model.loadProblem(matrix, vec_b_lo, vec_b_up, vec_c, vec_x_lo, vec_x_up);

    if (params->optimisation_mode == 0) {
        model.primal();
    } else {
        model.dual();
    }

    clp_result_t result;
    result.proven_optimal = model.isProvenOptimal();
    result.proven_dual_infeasible = model.isProvenDualInfeasible();
    result.proven_primal_infeasible = model.isProvenPrimalInfeasible();
    result.abandoned = model.isAbandoned();

    const double *x = model.getColSolution();
    assert(model.getNumCols() == mat_a->n_cols);
    for (int i = 0; i < model.getNumCols(); ++i) {
        vec_x_soln[i] = x[i];
    }
    
    return result;
}

