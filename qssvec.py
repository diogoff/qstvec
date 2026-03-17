import numba
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
        for basis, alpha in self.data.sort_index().items():
            key = f'{basis:0{self.num_qubits}b}'
            out[key] = alpha
        return out

    def evolve(self, operation, qargs):
        U = Operator(operation).data.astype(self.data.dtype)
        qargs = np.asarray(qargs, dtype=self.data.index.dtype)

        basis = self.data.index.values
        alpha = self.data.values

        basis, alpha = self._evolve_kernel(U, qargs, basis, alpha)

        new = pd.Series(data=alpha, index=basis)
        new = new.groupby(level=0).sum()

        new = new[new.abs() > 0.]

        self.data = new
        return self

    @staticmethod
    @numba.jit(nopython=True, parallel=True, cache=True)
    def _evolve_kernel(U, qargs, basis, alpha):
        dim = U.shape[0]
        n = basis.shape[0]

        col = np.zeros_like(basis)
        for i, q in enumerate(qargs):
            bit = (basis >> q) & 1
            col |= (bit << i)

        basis_ref = basis.copy()
        for q in qargs:
            basis_ref &= ~(1 << q)

        basis_out = np.empty(dim * n, dtype=basis.dtype)
        alpha_out = np.empty(dim * n, dtype=alpha.dtype)

        for row in numba.prange(dim):
            start = n * row
            end = start + n

            basis_out[start:end] = basis_ref
            for i, q in enumerate(qargs):
                if row & (1 << i):
                    basis_out[start:end] |= (1 << q)

            alpha_out[start:end] = U[row, col] * alpha
        
        return basis_out, alpha_out

    def truncate(self, p_frac=1., n_max=0):
        basis = self.data.index.values
        alpha = self.data.values

        basis, alpha = self._truncate_kernel(basis, alpha, p_frac, n_max)

        self.data = pd.Series(data=alpha, index=basis)
        return self

    @staticmethod
    @numba.jit(nopython=True, cache=True)
    def _truncate_kernel(basis, alpha, p_frac, n_max):
        prob = np.abs(alpha)**2
        idx = np.argsort(prob)[::-1]

        if 0. < p_frac < 1.:
            prob = prob[idx]
            frac = np.cumsum(prob) / np.sum(prob)
            n = np.searchsorted(frac, p_frac) + 1
            idx = idx[:n]

        if 0 < n_max < len(idx):
            idx = idx[:n_max]

        if 0 < len(idx) < len(basis):
            idx = np.sort(idx)
            basis = basis[idx]
            alpha = alpha[idx]
            alpha /= np.linalg.norm(alpha)

        return basis, alpha