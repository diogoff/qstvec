# qstvec

**qstvec** is a Python code for approximate simulation of quantum circuits based on a sparse and truncated state vector representation. It was originally developed for peaked circuits, where the goal is to find the most probable bit string.

## How to cite

If you find this code useful, please cite:

* Diogo R. Ferreira, *A Sparse and Truncated State Vector Simulator for Peaked Circuits*, 7th IEEE International Conference on Quantum Computing and Engineering (QCE26), 2026.

A machine-readable citation file is provided as `CITATION.cff`.

## Examples

In these examples, we use some circuits from BlueQubit's [Peaked Portal](https://app.bluequbit.io/hackathons) hackathon.

### Little peak

In this example, `little_peak.qasm` corresponds to BlueQubit's `P1_little_peak.qasm` circuit.

The script `little_peak.py` illustrates how to read the circuit and evolve the state vector, instruction by instruction, without any truncation.

At the end, it prints the most probable bit string.

### Sharp peak

In this example, `sharp_peak.qasm` corresponds to BlueQubit's `P3_sharp_peak.qasm` circuit.

The script `little_peak.py` implements the circuit simulation strategy (using blocks and gate fusion) described in the paper.

To use this script, specify the *k* for top-*k* truncation (default 0, no truncation) and/or the $p$ for $p$-mass truncation (default 1.0, no truncation).

For example:
* use `python sharp_peak.py 0 0.99` for a simulation with 99% of the probability mass;
* use `python sharp_peak.py 2**18 1.0` for a simulation with a maximum number of 2^18 terms.


### Test gates
