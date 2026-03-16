import numpy as np
import pandas as pd

from numba import jit
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

        # Call optimized kernel
        new_basis, new_alpha = self._evolve_kernel(U, qargs, basis, alpha)

        # Build new series
        new = pd.Series(data=new_alpha, index=new_basis)
        new = new.groupby(level=0).sum()

        # Filter out zeros
        new = new[new.abs() > 0.]

        # Update and return
        self.data = new
        return self

    @staticmethod
    @jit(nopython=True, cache=True)
    def _evolve_kernel(U, qargs, basis, alpha):
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

        # Preallocate arrays for the results
        new_basis = np.empty(n*dim, dtype=basis.dtype)
        new_alpha = np.empty(n*dim, dtype=alpha.dtype)
        idx = 0

        # Loop over rows of U
        for row in range(dim):
            # Corresponding output basis
            basis_out = basis_ref.copy()
            for i, q in enumerate(qargs):
                if row & (1 << i):
                    basis_out |= (1 << q)

            # Contribution to the output basis
            alpha_out = U[row, col] * alpha

            # Collect the results
            new_basis[idx:idx+n] = basis_out
            new_alpha[idx:idx+n] = alpha_out
            idx += n

        return new_basis, new_alpha

    def truncate(self, k, renorm=True):
        if 0 < k < len(self.data):
            mag = self.data.abs().values
            pos = np.argpartition(mag, -k)[-k:]
            new = pd.Series(data=self.data.values[pos],
                            index=self.data.index[pos])
            if renorm:
                norm = np.linalg.norm(new.values)
                new /= norm
            self.data = new
        return self