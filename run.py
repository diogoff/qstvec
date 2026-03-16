import sys
import time

from qiskit import QuantumCircuit
from qssvec import SparseStatevector

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} file.qasm')
    exit()

qc = QuantumCircuit.from_qasm_file(sys.argv[1])

sv = SparseStatevector(qc.num_qubits)

ci_num = 0

t0 = time.perf_counter()

for ci in qc.data:
    t1 = time.perf_counter()

    ci_num += 1

    name = ci.operation.name
    params = ci.operation.params
    qargs = [qc.find_bit(q).index for q in ci.qubits]

    sv = sv.evolve(ci.operation, qargs)
    
    k = 2**20
    sv = sv.truncate(k)
    n = len(sv.data)
   
    mag = sv.data.abs()
    idx = mag.idxmax()
    bit = f'{idx:0{qc.num_qubits}b}'
    amp = mag[idx]

    t2 = time.perf_counter()

    print()
    print(f'{ci_num}/{qc.size()} | {ci_num/qc.size()*100:.1f}%')
    print(f'{name} | {' '.join(map(str, params))} | {' '.join(map(str, qargs))}')
    print(f'{bit} | {amp:.3e}')
    print(f'{n} terms | max {k} | {k//n}x')
    print(f'{t2-t1:.1f} s/it | {(t2-t1)*(qc.size()-ci_num)/3600:.1f} hours')