import os
import sys
import math
import time
import psutil

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.quantum_info import ScalarOp
from qiskit.transpiler.passes import RemoveBarriers

from qssvec import SparseStatevector
#from qssvec_gpu import SparseStatevector

# -----------------------------------------------------------------------------

if len(sys.argv) < 4:
    print(f'Usage: python {sys.argv[0]} file.qasm p_frac n_max')
    exit()

fname = sys.argv[1]
p_frac = float(eval(sys.argv[2]))
n_max = int(eval(sys.argv[3]))

qc = QuantumCircuit.from_qasm_file(fname)
qc = RemoveBarriers()(qc)
qc.remove_final_measurements()

max_qubits = max([len(ci.qubits) for ci in qc.data])

# -----------------------------------------------------------------------------

dag = circuit_to_dag(qc)
blocks = []
qset_all = set()
qset_block = set()

def get_qset(node):
    return set(dag.find_bit(q).index for q in node.qargs)

def sort_key(node):
    qset_node = get_qset(node)
    return (len(qset_all | qset_node) - len(qset_all),
            len(qset_block | qset_node) - len(qset_block),
            tuple(sorted(qset_node)))

while dag.size() > 0:
    node = min(dag.front_layer(), key=sort_key)
    qset_node = get_qset(node)    
    dag.remove_op_node(node)

    if len(blocks) == 0:
        blocks.append([node])
        qset_block = qset_node
        qset_all = qset_node
        continue

    if qset_node.issubset(qset_block):
        blocks[-1].append(node)
        continue
    
    if len(qset_node.union(qset_block)) <= max_qubits:
        blocks[-1].append(node)
        qset_block |= qset_node
        qset_all |= qset_node
        continue

    blocks.append([node])
    qset_block = qset_node
    qset_all |= qset_node

# -----------------------------------------------------------------------------

sv = SparseStatevector(qc.num_qubits)

count_nodes = 0

t0 = time.perf_counter()

for k, block in enumerate(blocks, start=1):
    try:
        t1 = time.perf_counter()

        qargs = sorted(set([qc.find_bit(q).index for node in block for q in node.qargs]))
        U = ScalarOp(2 ** len(qargs), coeff=1.+0.j)
        
        for node in block:
            qargs_idx = [qargs.index(qc.find_bit(q).index) for q in node.qargs]
            U = U.compose(node.op, qargs=qargs_idx)

        sv.evolve(U.data, qargs)
        sv.truncate(p_frac=p_frac, n_max=n_max)
        b_str, prob = sv.bit_string(return_prob=True)

        print()

        count_nodes += len(block)
        print(f'{count_nodes}/{qc.size()} | {count_nodes/qc.size()*100.:.1f}%')
        print(f'{sys.argv[1]} | {qc.num_qubits} qubits | {qc.size()} gates')

        for node in block:
            qargs = set(qc.find_bit(q).index for q in node.qargs)
            print(f'| {node.op.name} {qargs}')

        print(f'{b_str} | prob {prob:.3e}')

        log = int(math.ceil(math.log2(len(sv))))
        mem = psutil.Process(os.getpid()).memory_info().vms / 1024**3
        print(f'{len(sv):,} terms | order 2^{log} | {mem:.1f} GB')

        t2 = time.perf_counter()

        print(f'elapsed {t2-t0:.1f} s | average {t2-t1:.1f} s/it | ', end='')
        eta = (t1 - t0) * (len(blocks) - k)
        if eta >= 3600:
            print(f'remaining {eta/3600:.1f} h')
        elif eta >= 60:
            print(f'remaining {eta/60:.1f} m')
        else:
            print(f'remaining {eta:.1f} s')

    except KeyboardInterrupt:
        break