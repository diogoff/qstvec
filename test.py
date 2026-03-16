from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from qssvec import SparseStatevector

qc = QuantumCircuit.from_qasm_file('test.qasm')
qc_size = qc.size()

n = qc.num_qubits
sv1 = Statevector.from_int(0, dims=2**n)
sv2 = SparseStatevector(n)

ci_num = 0
for ci in qc.data:
    ci_num += 1

    name = ci.operation.name
    params = ci.operation.params
    qargs = [qc.find_bit(q).index for q in ci.qubits]

    print(f'[{ci_num}/{qc_size}] {name} | {' '.join(map(str, params))} | {' '.join(map(str, qargs))}')

    sv1 = sv1.evolve(ci.operation, qargs)
    sv2 = sv2.evolve(ci.operation, qargs)

    d1 = sv1.to_dict()
    d2 = sv2.to_dict()

    if len(d1) != len(d2):
        print('Error: lengths do not match', len(d1), len(d2))
        exit()

    tol = 1e-12

    for key in sorted(set(d1.keys()) & set(d2.keys())):
        if abs(d1[key] - d2[key]) > tol:
            print('Error: values do not match', d1[key], d2[key])
            exit()
    
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