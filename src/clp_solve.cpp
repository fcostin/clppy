#include "clp_solve.h"

clp_result_t clp_solve(int n_rows, int n_cols, int n_entries,
        const int *row_indices, const int *col_indices,
        const double *coeffs, const double *vec_c,
        const double *vec_b_lo, const double *vec_b_up,
        const double *vec_x_lo, const double *vec_x_up,
        int optimisation_mode, double *vec_x_soln) {

    // XXX TODO will Coin delete our arrays?!

    printf("clp_solve : 0\n");
    
    // build column-packed coin sparse matrix from given COO data
    CoinPackedMatrix matrix(true, row_indices, col_indices,
        coeffs, (CoinBigIndex)n_entries);
    matrix.setDimensions(n_rows, n_cols);

    ClpSimplex model;

    model.loadProblem(matrix, vec_x_lo, vec_x_up, vec_c, vec_b_lo, vec_b_up);

    model.setOptimizationDirection(1.0); // minimise

    if (optimisation_mode == 0) {
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
    assert(model.getNumCols() == n_cols);
    for (int i = 0; i < model.getNumCols(); ++i) {
        vec_x_soln[i] = x[i];
    }
    
    return result;
}

