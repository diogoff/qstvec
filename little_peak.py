from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from qstvec import Statevector
#from qstvec_gpu import Statevector

qc = QuantumCircuit.from_qasm_file('little_peak.qasm')

sv = Statevector(qc.num_qubits)

for ci in qc.data:
    qargs = [qc.find_bit(q).index for q in ci.qubits]

    U = Operator(ci.operation).data
    sv = sv.evolve(U, qargs)

print(sv.bit_string())