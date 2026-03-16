import os
import sys
import math
import time
import psutil

from qiskit import QuantumCircuit
from qssvec import SparseStatevector

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} file.qasm')
    exit()

qc = QuantumCircuit.from_qasm_file(sys.argv[1])
qc_size = qc.size()

sv = SparseStatevector(qc.num_qubits)

ci_num = 0

t0 = time.perf_counter()

for ci in qc.data:

    ci_num += 1

    name = ci.operation.name
    params = ci.operation.params
    qargs = [qc.find_bit(q).index for q in ci.qubits]

    sv = sv.evolve(ci.operation, qargs)
    
    p_frac = 0.99
    sv = sv.truncate(p_frac)
    n = len(sv.data)
   
    mag = sv.data.abs()
    idx = mag.idxmax()
    bit = f'{idx:0{qc.num_qubits}b}'
    amp = mag[idx]

    pid = psutil.Process(os.getpid())
    mem = pid.memory_info().rss / 1024**3

    t1 = time.perf_counter()

    print()
    print(f'{ci_num}/{qc_size} | {ci_num/qc_size*100.:.1f}%')
    print(f'{name} | {' '.join(map(str, params))} | {' '.join(map(str, qargs))}')
    print(f'{bit} | {amp:.3e}')
    print(f'{n} terms | order 2^{int(math.ceil(math.log2(n)))} | mem {mem:.1f} GB')
    print(f'{t1-t0:.1f} s/it | {(t1-t0)*(qc_size-ci_num)/3600:.1f} hours')

    t0 = t1