# qstvec

**qstvec** is a Python code for approximate simulation of quantum circuits based on a sparse and truncated state vector representation. It was originally developed for peaked circuits, where the goal is to find the most probable bit string.

## Examples

In these examples, we use some circuits from BlueQubit's [*Peaked Portal*](https://app.bluequbit.io/hackathons) hackathon.

### Little peak

In this example, `little_peak.qasm` corresponds to BlueQubit's `P1_little_peak.qasm` circuit.

The script `little_peak.py` illustrates how to read the circuit and evolve the state vector, instruction by instruction, without any truncation.

At the end, it prints the most probable bit string.

### Sharp peak

### Test gates

## How to cite

If you find this code useful, please cite:

* Diogo R. Ferreira, *A Sparse and Truncated State Vector Simulator for Peaked Circuits*, 7th IEEE International Conference on Quantum Computing and Engineering (QCE26), 2026.

A machine-readable citation file is provided as `CITATION.cff`.