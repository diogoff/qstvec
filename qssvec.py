import numpy as np

class SparseStatevector:

    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.alpha = np.array([1.+0.j], dtype=np.complex128)
        self.basis = np.array([0], dtype=np.int64)

    def __len__(self):
        return len(self.basis)

    def to_dict(self):
        out = dict()
        for b, a in zip(self.basis, self.alpha):
            key = f'{b:0{self.n_qubits}b}'
            out[key] = a
        return out

    def evolve(self, U, qargs):
        alpha = self.alpha
        basis = self.basis

        U = np.asarray(U, dtype=alpha.dtype)
        qargs = np.asarray(qargs, dtype=basis.dtype)
        qrange = np.arange(qargs.size, dtype=basis.dtype)

        dim = 2 ** qargs.size
        assert U.shape == (dim, dim)

        bits = (basis[:, np.newaxis] >> qargs) & 1
        cols = np.sum(bits << qrange, axis=1)

        alpha_out = U[:, cols] * alpha[np.newaxis, :]
        alpha_out = alpha_out.ravel()

        rows = np.arange(U.shape[0])
        bits = (rows[:, np.newaxis] >> qrange) & 1
        bits = np.sum(bits << qargs, axis=1)

        basis_out = basis & ~np.sum(1 << qargs)
        basis_out = bits[:, np.newaxis] | basis_out[np.newaxis, :]
        basis_out = basis_out.ravel()

        basis, index = np.unique(basis_out, return_inverse=True)
        alpha = np.zeros(basis.shape, dtype=alpha.dtype)
        np.add.at(alpha, index, alpha_out)

        mask = np.abs(alpha) > 0.
        alpha = alpha[mask]
        basis = basis[mask]

        self.alpha = alpha
        self.basis = basis
        return self

    def truncate(self, p_frac=1., n_max=0):
        assert 0. <= p_frac <= 1.
        assert n_max >= 0

        alpha = self.alpha
        basis = self.basis

        probs = np.abs(alpha) ** 2
        index = np.argsort(probs)[::-1]

        if 0. < p_frac < 1.:
            probs = probs[index]
            p_fracs = np.cumsum(probs) / np.sum(probs)
            n = np.searchsorted(p_fracs, p_frac) + 1
            index = index[:n]

        if 0 < n_max < len(index):
            index = index[:n_max]

        if 0 < len(index) < len(basis):
            basis = basis[index]
            alpha = alpha[index]
            alpha /= np.linalg.norm(alpha)

        self.alpha = alpha
        self.basis = basis
        return self

    def bit_string(self, return_prob=False):
        probs = np.abs(self.alpha) ** 2
        i = np.argmax(probs)
        out = f'{self.basis[i]:0{self.n_qubits}b}'
        if return_prob:
            return out, probs[i]
        return out