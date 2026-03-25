import os
import sys
import math
import time
import psutil

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
qset = set()
seq = []

def get_node_qset(dag, node):
    return set(dag.find_bit(q).index for q in node.qargs)

def get_sort_key(dag, qset, node):
    node_qset = get_node_qset(dag, node)
    a = len(qset | node_qset)
    b = len(node_qset)
    c = tuple(sorted(node_qset))
    return (a, b, c)

while dag.size() > 0:
    key = lambda node: get_sort_key(dag, qset, node)
    node = sorted(dag.front_layer(), key=key)[0]
    dag.remove_op_node(node)
    seq.append(node)
    qset |= get_node_qset(dag, node)

# -----------------------------------------------------------------------------

n_seq = len(seq)
n_qubits = qc.num_qubits

sv = SparseStatevector(n_qubits)

for i, node in enumerate(seq, start=1):
    try:
        t0 = time.perf_counter()

        U = Operator(node.op).data
        qargs = [qc.find_bit(q).index for q in node.qargs]

        sv.evolve(U, qargs).truncate(0.999, 2**27)
        b_str, prob = sv.bit_string(return_prob=True)

        t1 = time.perf_counter()

        s_params = ' '.join(map(str, node.op.params))
        s_qargs = ' '.join(map(str, qargs))
        n_vec = len(sv)
        exp2 = int(math.ceil(math.log2(n_vec)))
        mem = psutil.Process(os.getpid()).memory_info().rss / 1024**3
        eta = (t1 - t0) * (n_seq - i) / 3600.

        print()
        print(f'{i}/{n_seq} | {i/n_seq*100.:.1f}%')
        print(f'{sys.argv[1]} | {n_qubits} qubits | {n_seq} gates')
        print(f'{node.op.name} | {s_params} | qargs {s_qargs}')
        print(f'{b_str} | prob {prob:.3e}')
        print(f'{n_vec} terms | order 2^{exp2} | {mem:.1f} GB')
        print(f'{t1-t0:.1f} s/it | {eta:.1f} hours')

    except KeyboardInterrupt:
        break