"""Use Topogonov's theorem to get a scattering matrix that approximates
a given unitary.
"""

import numpy as np
from numpy.typing import NDArray
from scipy.linalg import expm

from qoptcraft.operators import haar_random_unitary
from qoptcraft.basis import hilbert_dim, get_algebra_basis
from qoptcraft.math import gram_schmidt, mat_inner_product, mat_norm, logm_3
from qoptcraft.evolution import photon_unitary


def toponogov(matrix: NDArray, modes: int, photons: int, seed: int = None) -> tuple[NDArray, float]:
    """Use Topogonov's theorem to approximate a given unitary using linear optics.

    Args:
        matrix (NDArray): unitary matrix to approximate.
        modes (int): number of modes.
        photons (int): number of photons.

    Raises:
        ValueError: Matrix dimension doesn't match the number of modes and photons.

    Returns:
        NDArray, float: approximated unitary and the error.
    """
    dim = len(matrix)
    if dim != hilbert_dim(modes, photons):
        raise ValueError(f"Matrix {dim = } doesn't match with {photons = } and {modes = }.")

    basis, basis_image = get_algebra_basis(modes, photons)
    basis_image = gram_schmidt(basis_image)

    scattering_init = haar_random_unitary(modes, seed=seed)
    unitary = photon_unitary(scattering_init, photons, "hamiltonian")  # initial guess

    error: float = mat_norm(matrix - unitary)
    error_prev: float = 0

    while np.abs(error - error_prev) > 1e-8:
        unitary_inv = np.linalg.inv(unitary)
        log_unitary = logm_3(unitary_inv.dot(matrix))

        log_projected = np.zeros_like(unitary)  # Initialize to 0
        for basis_matrix in basis_image:
            coef = mat_inner_product(log_unitary, basis_matrix)
            log_projected += coef * basis_matrix

        unitary = unitary.dot(expm(log_projected))

        error_prev = error
        error = mat_norm(matrix - unitary)
    return unitary, error
