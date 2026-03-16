import os
import sys
import time
import psutil
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
    
    k = 2**20 # 2**28
    sv = sv.truncate(k)
   
    d = sv.to_dict()

    bit, amp = max(d.items(), key=lambda x: abs(x[1])**2)

    prob = abs(amp)**2

    n_terms = len(sv.data)
    mem_used = psutil.Process(os.getpid()).memory_info().rss / 1024**3
    mem_avail = psutil.virtual_memory().available / 1024**3

    t2 = time.perf_counter()

    print()
    print(f'{ci_num}/{qc.size()} | {ci_num/qc.size()*100:.1f}%')
    print(f'{name} | {' '.join(map(str, params))} | {' '.join(map(str, qargs))}')
    print(f'{bit} | {prob:.3e}')
    print(f'{n_terms} terms | max {k} | {k//n_terms}x')
    print(f'{mem_used:.1f} GB used | {mem_avail:.1f} GB available')
    print(f'{t2-t1:.1f} s/it | {(t2-t1)*(qc.size()-ci_num)/3600:.1f} hours')