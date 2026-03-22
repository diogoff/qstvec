import sys
import numpy as np

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag

# -----------------------------------------------------------------------------

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} file.qasm')
    exit()

qc = QuantumCircuit.from_qasm_file(sys.argv[1])

# -----------------------------------------------------------------------------

dag = circuit_to_dag(qc)

seen = set()
scheduled = []

while dag.op_nodes():
    front = dag.front_layer()

    candidates = []
    for node in front:
        qinds = [dag.find_bit(q).index for q in node.qargs]
        new_q = [q for q in qinds if q not in seen]
        candidates.append((len(new_q), -len(qinds) + len(new_q), node._node_id, node, qinds))




    
    break