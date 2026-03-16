import numpy as np
import pandas as pd

from qiskit.quantum_info import Operator

class SparseStatevector:

    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        alpha = 1.
        basis = pd.Index([0], dtype=np.int64)
        self.data = pd.Series(data=alpha, index=basis, dtype=np.complex128)

    def to_dict(self):
        out = dict()
        for basis, alpha in self.data.items():
            key = f'{basis:0{self.num_qubits}b}'
            out[key] = alpha
        return out

    def evolve(self, operation, qargs):
        # Unitary matrix for operation
        U = Operator(operation).data.astype(self.data.dtype)

        # Bases and amplitudes
        basis = self.data.index.values
        alpha = self.data.values

        # Dimensions
        dim = U.shape[0]
        n = basis.shape[0]

        # Column of U to be used
        col = np.zeros_like(basis)
        for i, q in enumerate(qargs):
            bit = (basis >> q) & 1
            col |= (bit << i)

        # Reference basis with zeroed bits
        basis_ref = basis.copy()
        for q in qargs:
            basis_ref &= ~(1 << q)

        # Arrays for storing the results
        new_basis = np.empty(dim * n, dtype=basis.dtype)
        new_alpha = np.empty(dim * n, dtype=alpha.dtype)

        # Loop over rows of U
        for row in range(dim):
            # Corresponding output basis
            basis_out = basis_ref.copy()
            for i, q in enumerate(qargs):
                if row & (1 << i):
                    basis_out |= (1 << q)

            # Contribution to the output basis
            alpha_out = U[row, col] * alpha

            # Write positions
            start = n * row
            end = start + n

            # Collect the results
            new_basis[start:end] = basis_out
            new_alpha[start:end] = alpha_out

        # Build new series
        new = pd.Series(data=new_alpha, index=new_basis)
        new = new.groupby(level=0).sum()

        # Filter out zeros
        new = new[new.abs() > 0.]

        # Update and return
        self.data = new
        return self

    def truncate(self, p_frac=1., n_max=0):
        basis = self.data.index.values
        alpha = self.data.values

        prob = np.abs(alpha)**2
        sort = np.argsort(prob)[::-1]
        prob = prob[sort]

        basis = basis[sort]
        alpha = alpha[sort]

        if 0. < p_frac < 1.:
            frac = np.cumsum(prob) / np.sum(prob)
            n = np.searchsorted(frac, p_frac) + 1
            basis = basis[:n]
            alpha = alpha[:n]

        if 0 < n_max < len(basis):
            basis = basis[:n_max]
            alpha = alpha[:n_max]

        alpha /= np.linalg.norm(alpha)

        self.data = pd.Series(data=alpha, index=basis)
        return self