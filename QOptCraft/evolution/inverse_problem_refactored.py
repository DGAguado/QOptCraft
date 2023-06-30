from itertools import permutations

# NumPy instalation: in the cmd: 'py -m pip install numpy'
import numpy as np
import sympy
from numpy.linalg import det, solve
from numpy.typing import NDArray
from numpy.lib.scimath import sqrt

from qoptcraft.operators import adjoint_evol
from qoptcraft.basis import get_algebra_basis, hilbert_dim
from qoptcraft.math import gram_schmidt, mat_inner_product


def scattering_from_photon_unitary(unitary: NDArray, modes: int, photons: int) -> NDArray:
    """_summary_

    Args:
        unitary (NDArray): _description_
        modes (int): _description_
        photons (int): _description_

    Returns:
        NDArray: _description_
    """
    dim = unitary.shape[0]
    if dim != hilbert_dim(modes, photons):
        raise ValueError("modes and photons don't match the dimension of the unitary.")
    _, basis_image = get_algebra_basis(modes, photons)
    dim = len(basis_image)
    basis_image = gram_schmidt(basis_image)
    coefs = np.zeros((dim, dim))
    rebuild_unitary = np.zeros((dim, dim))
    for i in range(dim):
        ad_matrix = adjoint_evol(basis_image[i], unitary)
        for j in range(dim):
            coef[i, j] = mat_inner_product(ad_matrix, basis_image[j])
        for j in range(dim):
            try:
                coefs[i, j] = solve(image_matrix[i, j], ad_matrix[i, j])
            except 
    return coefs


def scattering_from_photon_unitary_sympy(unitary: NDArray, modes: int, photons: int) -> NDArray:
    """_summary_

    Args:
        unitary (NDArray): _description_
        modes (int): _description_
        photons (int): _description_

    Returns:
        NDArray: _description_
    """
    _, basis_image = get_algebra_basis(modes, photons)
    dim = len(basis_image)
    coefs = np.zeros((dim, dim))
    sym_coefs = sympy.MatrixSymbol("coefs", dim, dim)
    for i, matrix in enumerate(basis_image):
        ad_matrix = adjoint_evol(matrix, unitary)
        image_matrix = np.zeros((dim, dim))
        for j, basis_matrix in enumerate(basis_image):
            image_matrix += sym_coefs[i, j] * basis_matrix
        for j in range(dim):
            try:
                coefs[i, j] = solve(image_matrix[i, j], ad_matrix[i, j])
            except 
    return coefs

def SfromU(unitary: NDArray, modes: int, photons: int):
    """Calculates a linear optics scattering matrix that is lifted
    to the given unitary.
    """
    basis, basis_image = get_algebra_basis(modes, photons)
    for matrix in basis_image:
        adjoint_evol(matrix, unitary)
    # We obtain the equation system
    eq_sys, eq_sys_choice, index_choice = eq_sys_finder(basis, basis_image)
    # Verification of the system's validity; in case it is computable, the solution is obtained
    # In case it is not, "None" is given instead
    sol, sol_e, sol_f, check_sol = verification(
        U,
        base_u_m,
        base_u_m_e,
        base_u_m_f,
        separator_e_f,
        base_u_M,
        eq_sys,
        eq_sys_choice,
        index_choice,
    )
    S = False
    if perm is True:
        perm_iterator = permutations(range(M))
        for item in perm_iterator:
            # U_perm_file.write(f"\n\nU (permutación {np.asarray(item)}):\n")
            # We compute the permutation matrix...
            M_perm = permutation_matrix(np.asarray(item))
            # Which we apply at both sides of the matrix U_perm for the basis change
            U_perm = M_perm.dot(U.dot(np.transpose(M_perm)))
            # We verify the solution's existence again, this time for each permutation
            sol, sol_e, sol_f, check_sol = verification(
                U_perm,
                base_u_m,
                base_u_m_e,
                base_u_m_f,
                separator_e_f,
                base_u_M,
                eq_sys,
                eq_sys_choice,
                index_choice,
            )
            if check_sol:  # ==True, implied
                S_perm = S_output(base_u_m, base_U_m, sol_e, sol_f)
    return S, S_perm


def permutation_matrix(perm_list):
    N = len(perm_list)
    I = np.identity(N, dtype=int)
    M = np.identity(N, dtype=int)
    for i in range(N):
        M[i] = I[perm_list[i]]
    return M


# A selection of linear independent equations is obtained
def eq_sys_finder(basis_algebra, basis_image_algebra):
    m = len(basis_algebra[0])
    M = len(basis_image_algebra[0])
    # Equation system initialization
    eq_sys = np.zeros((M * M, m * m), dtype=complex)
    # Storage of all the present equations in the system
    for j in range(m * m):
        for l in range(M):
            for o in range(M):
                eq_sys[M * l + o, j] = basis_image_algebra[j, l, o]
    # Array wich storages m*m equations of eq_sys, for which we will attempt to solve the system
    # We will use np.append() in this and the following array for adding new terms
    eq_sys_choice = np.zeros((1, m * m), dtype=complex)
    # Array which storages the indexes of the chosen equations
    index_choice = np.zeros(1, dtype=int)
    cont = 0
    end = False
    # This loop searches for m*m equations of the list eq_sys for which a matrix with
    # a no-null determinant is made. That is, they are linear independent
    for l in range(M):
        for o in range(M):
            if cont > 0:
                # With this functions, we conserve the linear independent rows
                aux, inds = sympy.Matrix(eq_sys_choice).T.rref()
                # Applying inds to our two arrays, the algorithm is still ongoing until...
                eq_sys_choice = np.array(eq_sys_choice[np.array(inds)])
                index_choice = np.array(index_choice[np.array(inds)])
            # By obtaining a m*m x m*m equation system, with a no-null determinant, we have
            # computed the required system
            if len(eq_sys_choice[0]) == len(eq_sys_choice[:, 0]) and det(eq_sys_choice) != 0:
                end = True
                break
            # This simple condition saves multiple steps of null vectors being eliminated
            elif (eq_sys[M * l + o] != 0).any():
                if cont == 0:
                    eq_sys_choice[cont] = eq_sys[M * l + o]
                    index_choice[cont] = M * l + o
                else:
                    # We add the new arrays
                    eq_sys_choice = np.append(eq_sys_choice, np.array([eq_sys[M * l + o]]), axis=0)
                    index_choice = np.append(index_choice, np.array([M * l + o]), axis=0)
                cont += 1
        if end is True:
            break
    return eq_sys, eq_sys_choice, index_choice


def verification(
    U, base_u_m, base_u_m_e, base_u_m_f, sep, base_u_M, eq_sys, eq_sys_choice, index_choice
):
    m = len(base_u_m[0])
    M = len(base_u_M[0])
    # Solution arrays initialization
    sol = np.zeros((m * m, m * m), dtype=complex)
    sol_e = np.zeros((m * m, m * m), dtype=complex)
    sol_f = np.zeros((m * m, m * m), dtype=complex)
    # Saving both basis of the u(m) and u(M) subspaces
    for j in range(m * m):
        # We compute the adjoint for each matrix in the basis of u(M)
        adj_U_b_j = adjoint_evol(base_u_M[j], U)
        adj_U_b_j_reshape = np.reshape(adj_U_b_j, M * M)
        # We choose the adj_U_b_j values of the indexes corresponding to the used equations
        adj_U_b_j_choice = np.array(adj_U_b_j_reshape[np.array(index_choice)])
        sol[j] = solve(eq_sys_choice, adj_U_b_j_choice)
        # Check for its validity for all possible equations?
        for l in range(M * M):
            suma = 0
            for o in range(m * m):
                suma += eq_sys[l, o] * sol[j, o]
            if np.round(suma, 8) != np.round(adj_U_b_j_reshape[l], 8):
                op = np.array([None])
                check = False
                # We return it three times for keeping consistency with the main algorithm 3
                return op, op, op, check
    # If the algorithm reaches this line, the solution exists. It is computed, giving a general solution of all
    # equations, and a separated version only applied to the e_jk and f_jk respectively, useful in the reconstruction of S
    check = True
    for j in range(m):
        for k in range(m):
            if m * j + k < sep:
                for l in range(m * m):
                    if (base_u_m_e[l] == base_u_m[m * j + k]).all():
                        sol_e[l] = sol[m * j + k]
            else:
                for l in range(m * m):
                    if (base_u_m_f[l] == base_u_m[m * j + k]).all():
                        sol_f[l] = sol[m * j + k]
                    if (base_u_m_f[l] == -base_u_m[m * j + k]).all():
                        sol_f[l] = -sol[m * j + k]
    return sol, sol_e, sol_f, check


def S_output(base_u_m, base_U_m, sol_e, sol_f):
    m = len(base_u_m[0])
    S = np.zeros((m, m), dtype=complex)
    # First of all, we obtain a no-null value of S for using it as a base for the rest computations
    for l in range(m):
        end = False
        for j in range(m):
            l_array = np.array([base_U_m[l]])
            absS = -1j * np.conj(l_array).dot(
                adjoint_S(m * j + j, base_u_m, sol_e).dot(np.transpose(l_array))
            )
            # 8 decimal accuracy, it can be modified
            if np.round(absS, 8) == 0:
                S[l, j] = 0
            else:
                # We ignore the offset (for now...)
                l0 = l
                j0 = j
                end = True
                break
        if end:
            break

    # Later, we compute the total matrix. l0 y j0 serve as a support
    for l in range(m):
        for j in range(m):
            l0_array = np.array([base_U_m[l0]])

            l_array = np.array([base_U_m[l]])

            j_array = np.array([base_U_m[j]])
            # Storage of the sum in S
            S += (
                (
                    np.conj(l_array).dot(
                        adjoint_S(m * j + j0, base_u_m, sol_f).dot(np.transpose(l0_array))
                    )
                    - 1j
                    * np.conj(l_array).dot(
                        adjoint_S(m * j + j0, base_u_m, sol_e).dot(np.transpose(l0_array))
                    )
                )
                / sqrt(
                    -1j
                    * np.conj(l0_array).dot(
                        adjoint_S(m * j0 + j0, base_u_m, sol_e).dot(np.transpose(l0_array))
                    )
                )
                * (np.transpose(l_array).dot(np.conj(j_array)))
            )
    return S


def adjoint_S(index, base_u_m, sol):
    m = len(base_u_m[0])

    suma = np.zeros((m, m), dtype=complex)

    for j in range(m * m):
        suma += sol[index, j] * base_u_m[j]

    return suma
