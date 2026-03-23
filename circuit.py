import sys
import copy

from qiskit import QuantumCircuit
from qiskit.circuit import CircuitInstruction
from qiskit.converters import circuit_to_dag

# -----------------------------------------------------------------------------

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} file.qasm')
    exit()

qc = QuantumCircuit.from_qasm_file(sys.argv[1])

# -----------------------------------------------------------------------------

output_seq = []

def traverse(current_dag, current_qset, current_seq):
    if current_dag.size() == 0:
        if not output_seq:
            output_seq = copy.deepcopy(current_seq)
        else:
            better = False
            for i in range(current_seq):
                if current_seq[i][0] < output_seq[i][0]:
                    better = True
                    break
            if better:
                output_seq = copy.deepcopy(current_seq)
        return

    while True:
        front_nodes = dict()
        for node in current_dag.front_layer():
            qset = frozenset(node.qargs)
            if qset not in front_nodes:
                front_nodes[qset] = []
            front_nodes[qset].append(node)

        if len(front_nodes) == 0:
            output_seqs.append(current_seq)
            return

        ready_nodes = dict()
        for qset in front_nodes:
            if qset <= current_qset:
                ready_nodes[qset] = front_nodes[qset]

        if len(ready_nodes) == 0:
            break

        for qset in ready_nodes:
            for node in ready_nodes[qset]:
                current_dag.remove_op_node(node)
                current_seq.append((qset, node))

    for qset in front_nodes:
        new_current_qset = current_qset | qset
        new_current_dag = copy.deepcopy(current_dag)
        new_current_seq = copy.deepcopy(current_seq)
        for node in front_nodes[qset]:
            new_current_dag.remove_op_node(node)
            new_current_seq.append((qset, node))
        traverse(new_current_dag, new_current_qset, new_current_seq, output_seq)

# -----------------------------------------------------------------------------


for q in range(qc.num_qubits):
    current_dag = circuit_to_dag(qc)
    current_qset = frozenset({current_dag.qubits[q]})
    current_seq = []
    traverse(current_dag, current_qset, current_seq, output_seq)

print(f'Sequence with {len(output_seq)} instructions:')
for i, node in enumerate(output_seq):
    name = node.op.name
    qind = [qc.find_bit(q).index for q in node.qargs]
    print(f'{i+1}) {node.op.name} {' '.join(map(str, qind))}')