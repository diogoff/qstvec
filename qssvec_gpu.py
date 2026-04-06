import cupy as cp

class SparseStatevector:
    _dtype_complex = cp.complex128
    _dtype_float = cp.float64
    _dtype_int = cp.int64

    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.alpha = cp.array([1.+0.j], dtype=self._dtype_complex)
        self.basis = cp.array([0], dtype=self._dtype_int)

    def __len__(self):
        return len(self.basis)

    def to_dict(self):
        n = self.n_qubits
        alpha = self.alpha.get()
        basis = self.basis.get()
        return {f'{b:0{n}b}': a for a, b in zip(alpha, basis)}

    def evolve(self, U, qargs):
        alpha = self.alpha
        basis = self.basis

        U = cp.asarray(U, dtype=self._dtype_complex)
        qargs = cp.asarray(qargs, dtype=self._dtype_int)
        qrange = cp.arange(len(qargs), dtype=self._dtype_int)

        cols = (basis[:, cp.newaxis] >> qargs) & 1
        cols = cp.sum(cols << qrange, axis=1)

        alpha_out = U[:, cols] * alpha[cp.newaxis, :]
        alpha_out = alpha_out.ravel()

        bits = cp.arange(U.shape[0], dtype=self._dtype_int)
        bits = (bits[:, cp.newaxis] >> qrange) & 1
        bits = cp.sum(bits << qargs, axis=1)

        basis_out = basis & ~cp.sum(1 << qargs)
        basis_out = bits[:, cp.newaxis] | basis_out[cp.newaxis, :]
        basis_out = basis_out.ravel()

        basis, index = cp.unique(basis_out, return_inverse=True)

        alpha_real = cp.zeros(basis.shape, dtype=self._dtype_float)
        alpha_imag = cp.zeros(basis.shape, dtype=self._dtype_float)

        cp.add.at(alpha_real, index, alpha_out.real)
        cp.add.at(alpha_imag, index, alpha_out.imag)

        alpha = alpha_real + 1.j * alpha_imag

        mask = cp.abs(alpha) > 0.
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

        probs = cp.abs(alpha) ** 2
        index = cp.argsort(probs)[::-1]

        if 0. < p_frac < 1.:
            probs = probs[index]
            probs = cp.cumsum(probs) / cp.sum(probs)
            n = cp.searchsorted(probs, p_frac) + 1
            index = index[:n]

        if 0 < n_max < len(index):
            index = index[:n_max]

        if 0 < len(index) < len(basis):
            basis = basis[index]
            alpha = alpha[index]
            alpha /= cp.linalg.norm(alpha)

        self.alpha = alpha
        self.basis = basis
        return self

    def bit_string(self, return_prob=False):
        probs = cp.abs(self.alpha) ** 2
        i = cp.argmax(probs).item()
        b = self.basis[i].item()
        n = self.n_qubits
        if return_prob:
            return f'{b:0{n}b}', probs[i]
        return f'{b:0{n}b}'