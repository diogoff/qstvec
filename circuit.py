import os
import sys
import math
import time
import psutil
import numpy as np

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.quantum_info import Operator

from qssvec import SparseStatevector

# -----------------------------------------------------------------------------

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} file.qasm')
    exit()

qc = QuantumCircuit.from_qasm_file(sys.argv[1])

# -----------------------------------------------------------------------------

dag = circuit_to_dag(qc)
blocks = []
current_qset = set()

def get_node_qset(node):
    return set(dag.find_bit(q).index for q in node.qargs)

def get_sort_key(node):
    node_qset = get_node_qset(node)
    a = len(current_qset | node_qset)
    b = len(node_qset)
    c = tuple(sorted(node_qset))
    return (a, b, c)

while dag.size() > 0:
    node = sorted(dag.front_layer(), key=get_sort_key)[0]
    node_qset = get_node_qset(node)    
    dag.remove_op_node(node)

    if len(blocks) == 0:
        blocks.append([node])
        current_qset = node_qset
        continue

    if node_qset.issubset(current_qset):
        blocks[-1].append(node)
        continue

    if node_qset.isdisjoint(current_qset):
        blocks.append([node])
        current_qset = node_qset
        continue
    
    if len(current_qset) < 2:
        blocks[-1].append(node)
        current_qset |= node_qset
        continue

    blocks.append([node])
    current_qset = node_qset

# -----------------------------------------------------------------------------

sv = SparseStatevector(qc.num_qubits)

n_done = 0

for k, block in enumerate(blocks, start=1):
    try:
        t0 = time.perf_counter()

        qargs = sorted(set([qc.find_bit(q).index for node in block for q in node.qargs]))
        U = Operator(np.eye(2 ** len(qargs), dtype=complex))
        
        for node in block:
            qargs_idx = [qargs.index(qc.find_bit(q).index) for q in node.qargs]
            U = U.compose(Operator(node.op), qargs=qargs_idx)

        sv.evolve(U.data, qargs)
        sv.truncate(p_frac=0.999, n_max=2**20)
        b_str, prob = sv.bit_string(return_prob=True)

        t1 = time.perf_counter()

        print()
        n_done += len(block)
        print(f'{n_done}/{qc.size()} | {n_done/qc.size()*100.:.1f}%')
        print(f'{sys.argv[1]} | {qc.num_qubits} qubits | {qc.size()} gates')
        for node in block:
            s_params = ' '.join(map(str, node.op.params))
            s_qargs = ' '.join(map(str, [qc.find_bit(q).index for q in node.qargs]))
            print(f'{node.op.name} | {s_params} | qargs {s_qargs}')
        print(f'{b_str} | prob {prob:.3e}')
        n_vec = len(sv)
        exp2 = int(math.ceil(math.log2(n_vec)))
        mem = psutil.Process(os.getpid()).memory_info().vms / 1024**3
        print(f'{n_vec:,} terms | order 2^{exp2} | {mem:.1f} GB')
        eta = (t1 - t0) * (len(blocks) - k) / 3600.
        print(f'{t1-t0:.1f} s/it | {eta:.1f} hours')

    except KeyboardInterrupt:
        break