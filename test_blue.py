import sys
import bluequbit

from qiskit import QuantumCircuit

# -----------------------------------------------------------------------------

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} file.qasm')
    exit()

qc = QuantumCircuit.from_qasm_file(sys.argv[1])

# -----------------------------------------------------------------------------

bq = bluequbit.init("cWnKawhJwdl3XbUXma7dveMyI6zkCgmz")

result = bq.run(qc, device='mps.cpu', shots=100)

counts = result.get_counts()
counts = sorted(counts.items(), key=lambda x: x[1])
for basis, count in counts:
    print(count, ':', basis)