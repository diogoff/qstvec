# qstvec

**qstvec** is a Python code for approximate simulation of quantum circuits based on a sparse and truncated state vector representation.

It was originally developed for peaked circuits, where the goal is to find the most probable bit string.

## Examples

In these examples, we use some circuits from BlueQubit's [Peaked Portal](https://app.bluequbit.io/hackathons) hackathon.

### Little peak

In this example, `little_peak.qasm` corresponds to BlueQubit's `P1_little_peak.qasm` circuit.

The script `little_peak.py` illustrates how to read the circuit and evolve the state vector, instruction by instruction, without any truncation.

At the end, it prints the most probable bit string.

### Sharp peak

In this example, `sharp_peak.qasm` corresponds to BlueQubit's `P3_sharp_peak.qasm` circuit.

The script `little_peak.py` implements the circuit simulation strategy (block-based) described in the paper (see below).

To use this script, specify the *k* for top-*k* truncation (default 0, no truncation) and/or the $p$ for $p$-mass truncation (default 1.0, no truncation).

For example:
* use `python sharp_peak.py 0 0.99` for a simulation with a fraction of the probability mass (99%).
* use `python sharp_peak.py 2**18 1.0` for a simulation with a limit on the number of terms (2<sup>18</sup>).

### Test gates

This example ensures that the results are fully consistent with a state vector simulation via [qiskit](https://github.com/Qiskit/qiskit).

For this purpose, `test_gates.qasm` contains an example for all the standard gates available in OpenQASM 2.0 ([qelib1.inc](https://github.com/Qiskit/qiskit/blob/main/qiskit/qasm/libs/qelib1.inc)).

The script `test_gates.py` evolves qiskit's `Statevector` and qstvec's `Statevector` side-by-side, and checks that the bit strings and probabilities match after each circuit instruction.

## How to cite

If you find this code useful, please cite the paper:

* Diogo R. Ferreira, *A Sparse and Truncated State Vector Simulator for Peaked Circuits*, 7th IEEE International Conference on Quantum Computing and Engineering (QCE26), 2026.
