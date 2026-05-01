from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector as Statevector1
from qiskit.quantum_info import Operator

from qstvec import Statevector as Statevector2
#from qstvec_gpu import Statevector as Statevector2

qc = QuantumCircuit.from_qasm_file('test_gates.qasm')
qc_size = qc.size()

n = qc.num_qubits
sv1 = Statevector1.from_int(0, dims=2**n)
sv2 = Statevector2(n)

ci_num = 0
for ci in qc.data:
    ci_num += 1

    name = ci.operation.name
    params = ci.operation.params
    qargs = [qc.find_bit(q).index for q in ci.qubits]

    print(f'[{ci_num}/{qc_size}] {name} | {' '.join(map(str, params))} | {' '.join(map(str, qargs))}')

    sv1 = sv1.evolve(ci.operation, qargs)

    U = Operator(ci.operation).data
    sv2 = sv2.evolve(U, qargs).truncate()

    d1 = sv1.to_dict()
    d2 = sv2.to_dict()

    if len(d1) != len(d2):
        print('Error: lengths do not match', len(d1), len(d2))
        exit()

    tol = 1e-12
    
    bit1, amp1 = max(d1.items(), key=lambda x: abs(x[1])**2)
    bit2, amp2 = max(d2.items(), key=lambda x: abs(x[1])**2)

    if bit1 != bit2:
        print('Error: bitstrings do not match', bit1, bit2)
        exit()

    prob1 = abs(amp1)**2
    prob2 = abs(amp2)**2

    if abs(prob1 - prob2) > tol:
        print('Error: probabilities do not match', prob1, prob2)
        exit()

    print(f'[{ci_num}/{qc_size}] {bit1}: {prob1:.6f} | {bit2}: {prob2:.6f}')