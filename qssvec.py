import numpy as np
import pandas as pd

from qiskit.quantum_info import Operator

class SparseStatevector:

    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        alpha = 1.
        basis = pd.Index([0], dtype=int)
        self.data = pd.Series(data=alpha, index=basis, dtype=complex)

    def to_dict(self):
        out = dict()
        for basis, alpha in self.data.items():
            key = f'{basis:0{self.num_qubits}b}'
            out[key] = alpha
        return out

    def evolve(self, operation, qargs):
        # Unitary matrix for operation
        U = Operator(operation).data

        # Expected matrix dimension
        dim = 1 << len(qargs)
        assert U.shape == (dim, dim)

        # Bases and amplitudes
        basis = self.data.index.values
        alpha = self.data.values

        # Column of U to be used
        col = np.zeros_like(basis)
        for i, q in enumerate(qargs):
            b = (basis >> q) & 1
            col |= (b << i)

        # Reference basis with zeroed bits
        basis_ref = basis.copy()
        for q in qargs:
            basis_ref &= ~(1 << q)

        # Accumulator for new data
        new = pd.Series(dtype=self.data.dtype)

        # Loop over rows of U
        for row in range(dim):

            # Corresponding output basis
            basis_out = basis_ref.copy()
            for i, q in enumerate(qargs):
                if row & (1 << i):
                    basis_out |= (1 << q)

            # Contribution to the output basis
            amp = U[row, col] * alpha
            amp = pd.Series(data=amp, index=basis_out)
            amp = amp.groupby(level=0).sum()

            # Accumulate in new data
            new = new.add(amp, fill_value=0.)

        # Filter out zeros
        new = new[new.abs() > 0.]

        # Update and return
        self.data = new
        return self

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