import numpy as np

class Statevector:
    _dtype_complex = np.complex128
    _dtype_int = np.int64

    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.alpha = np.array([1.+0.j], dtype=self._dtype_complex)
        self.basis = np.array([0], dtype=self._dtype_int)

    def __len__(self):
        return len(self.basis)

    def to_dict(self):
        n = self.n_qubits
        alpha = self.alpha
        basis = self.basis
        return {f'{b:0{n}b}': a for a, b in zip(alpha, basis)}

    def evolve(self, U, qargs):
        alpha = self.alpha
        basis = self.basis

        U = np.asarray(U, dtype=self._dtype_complex)
        qargs = np.asarray(qargs, dtype=self._dtype_int)
        qrange = np.arange(len(qargs), dtype=self._dtype_int)

        cols = (basis[:, np.newaxis] >> qargs) & 1
        cols = np.sum(cols << qrange, axis=1)

        alpha_out = U[:, cols] * alpha[np.newaxis, :]
        alpha_out = alpha_out.ravel()

        bits = np.arange(U.shape[0], dtype=self._dtype_int)
        bits = (bits[:, np.newaxis] >> qrange) & 1
        bits = np.sum(bits << qargs, axis=1)

        basis_out = basis & ~np.sum(1 << qargs)
        basis_out = bits[:, np.newaxis] | basis_out[np.newaxis, :]
        basis_out = basis_out.ravel()

        basis, index = np.unique(basis_out, return_inverse=True)
        alpha = np.zeros(basis.shape, dtype=self._dtype_complex)
        np.add.at(alpha, index, alpha_out)

        mask = np.abs(alpha) > 0.
        alpha = alpha[mask]
        basis = basis[mask]

        self.alpha = alpha
        self.basis = basis
        return self

    def truncate(self, k_top=0, p_frac=1.):
        assert k_top >= 0
        assert 0. <= p_frac <= 1.

        alpha = self.alpha
        basis = self.basis

        probs = np.abs(alpha) ** 2
        index = np.argsort(probs)[::-1]

        if 0. < p_frac < 1.:
            probs = probs[index]
            probs = np.cumsum(probs) / np.sum(probs)
            k = np.searchsorted(probs, p_frac) + 1
            index = index[:k]

        if 0 < k_top < len(index):
            index = index[:k_top]

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
        b = self.basis[i]
        n = self.n_qubits
        if return_prob:
            return f'{b:0{n}b}', probs[i]
        return f'{b:0{n}b}'