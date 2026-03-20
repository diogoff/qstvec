import os
import sys
import math
import time
import psutil

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from qssvec import SparseStatevector

# -----------------------------------------------------------------------------

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} file.qasm')
    exit()

qc = QuantumCircuit.from_qasm_file(sys.argv[1])

qc_size = qc.size()

# -----------------------------------------------------------------------------

layers = []
last_layer_i = [-1] * qc.num_qubits

for ci in qc.data:
    qset = set([qc.find_bit(q).index for q in ci.qubits])

    i0 = 0
    for q in qset:
        if last_layer_i[q] > i0:
            i0 = last_layer_i[q]

    best_overlap = 0
    best_layer_i = -1

    for i in range(i0, len(layers)):
        overlap = len(layers[i][0] & qset)
        if overlap > best_overlap:
            best_overlap = overlap
            best_layer_i = i

    if best_overlap > 0:
        i = best_layer_i
        layers[i][0] |= qset
        layers[i][1] += [ci]
    else:
        i = len(layers)
        layer = [qset, [ci]]
        layers.append(layer)
    
    for q in qset:
        if i > last_layer_i[q]:
            last_layer_i[q] = i


for i, layer in enumerate(layers):
    print(f'layer {i+1} | qset {' '.join(map(str, layer[0]))} | gates {len(layer[1])}')

exit()

# -----------------------------------------------------------------------------

sv = SparseStatevector(qc.num_qubits)

ci_num = 0

t0 = time.perf_counter()

for layer in layers:
    for ci in layer[1]:
        ci_num += 1

        name = ci.operation.name
        params = ci.operation.params
        qargs = [qc.find_bit(q).index for q in ci.qubits]
        qargs = [qc.find_bit(q).index for q in ci.qubits]

        U = Operator(ci.operation).data
        sv = sv.evolve(U, qargs)
        
        p_frac = 0.999
        sv = sv.truncate(p_frac)
        n = len(sv.data)
    
        mag = sv.data.abs()
        idx = mag.idxmax()
        bit = f'{idx:0{qc.num_qubits}b}'
        mag = mag[idx]

        pid = psutil.Process(os.getpid())
        mem = pid.memory_info().rss / 1024**3

        t1 = time.perf_counter()

        print()
        print(f'{ci_num}/{qc_size} | {ci_num/qc_size*100.:.1f}%')
        print(f'{name} | {' '.join(map(str, params))} | qubit {' '.join(map(str, qargs))}')
        print(f'{bit} | mag {mag:.3e}')
        print(f'{n} terms | order 2^{int(math.ceil(math.log2(n)))} | mem {mem:.1f} GB')
        print(f'{t1-t0:.1f} s/it | {(t1-t0)*(qc_size-ci_num)/3600:.1f} hours')

        t0 = t1