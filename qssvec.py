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
        alpha = self.data.values
        basis = self.data.index.values

        U = Operator(operation).data.astype(alpha.dtype)
        qargs = np.asarray(qargs)
        qrange = np.arange(qargs.size)

        dim = 2 ** qargs.size
        assert U.shape == (dim, dim)

        bits = (basis[:, np.newaxis] >> qargs) & 1
        cols = np.bitwise_or.reduce(bits << qrange, axis=1)

        alpha_out = U[:, cols] * alpha[np.newaxis, :]
        alpha_out = alpha_out.ravel()

        rows = np.arange(dim)
        bits = (rows[:, np.newaxis] >> qrange) & 1
        bits = np.bitwise_or.reduce(bits << qargs, axis=1)

        basis_out = basis & ~np.bitwise_or.reduce(1 << qargs)
        basis_out = basis_out[np.newaxis, :] | bits[:, np.newaxis]
        basis_out = basis_out.ravel()

        new = pd.Series(data=alpha_out, index=basis_out)
        new = new.groupby(level=0).sum()
        new = new[new.abs() > 0.]

        self.data = new
        return self

    def truncate(self, p_frac=1., n_max=0):
        assert 0. <= p_frac <= 1.
        assert n_max >= 0

        alpha = self.data.values
        basis = self.data.index.values

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
            norm = np.linalg.norm(alpha)
            if norm > 0.:
                alpha /= norm

        self.data = pd.Series(data=alpha, index=basis)
        return self