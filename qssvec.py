import numpy as np

class SparseStatevector:

    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.alpha = np.array([1.+0.j], dtype=np.complex128)
        self.basis = np.array([0], dtype=np.int64)

    def __len__(self):
        return len(self.basis)

    def to_dict(self):
        out = dict()
        index = np.argsort(self.basis)
        for basis, alpha in zip(self.basis[index], self.alpha[index]):
            key = f'{basis:0{self.num_qubits}b}'
            out[key] = alpha
        return out

    def evolve(self, U, qargs):
        alpha = self.alpha
        basis = self.basis

        U = U.astype(alpha.dtype)
        qargs = np.asarray(qargs)
        qrange = np.arange(qargs.size)

        dim = 2 ** qargs.size
        assert U.shape == (dim, dim)

        bits = (basis[:, np.newaxis] >> qargs) & 1
        cols = np.bitwise_or.reduce(bits << qrange, axis=1)

        alpha_out = U[:, cols] * alpha[np.newaxis, :]
        alpha_out = alpha_out.ravel()

        rows = np.arange(U.shape[0])
        bits = (rows[:, np.newaxis] >> qrange) & 1
        bits = np.bitwise_or.reduce(bits << qargs, axis=1)

        basis_out = basis & ~np.bitwise_or.reduce(1 << qargs)
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

        probs = np.abs(alpha)**2
        index = np.argsort(probs)[::-1]

        if 0. < p_frac < 1.:
            probs = probs[index]
            p_fracs = np.cumsum(probs) / np.sum(probs)
            n = np.searchsorted(p_fracs, p_frac) + 1
            index = index[:n]

        if 0 < n_max < len(index):
            index = index[:n_max]

        if 0 < len(index) < len(basis):
            index = np.sort(index)
            basis = basis[index]
            alpha = alpha[index]
            norm = np.linalg.norm(alpha)
            if norm > 0.:
                alpha /= norm

        self.alpha = alpha
        self.basis = basis
        return self

    def bit_string(self, return_prob=False):
        idx = np.argmax(np.abs(self.alpha))
        out = f'{self.basis[idx]:0{self.num_qubits}b}'
        if return_prob:
            prob = np.abs(self.alpha[idx])**2
            return out, prob
        else:
            return out