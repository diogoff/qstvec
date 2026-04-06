import sys
import bluequbit

from qiskit import QuantumCircuit
from qiskit.transpiler.passes import RemoveBarriers

# -----------------------------------------------------------------------------

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} file.qasm')
    exit()

qc = QuantumCircuit.from_qasm_file(sys.argv[1])
qc = RemoveBarriers()(qc)
qc.remove_final_measurements()

# -----------------------------------------------------------------------------

bq = bluequbit.init('cWnKawhJwdl3XbUXma7dveMyI6zkCgmz')

result = bq.run(qc, device='mps.gpu', shots=100)
counts = result.get_counts()
counts = max(counts.items(), key=lambda x: x[1])

print(counts[0])