# qstvec

**qstvec** is a Python package for approximate simulation of quantum circuits based on a sparse and truncated state vector representation.

It was originally developed for peaked circuits, where the goal is to find the most probable output bit string.

When only a small fraction of basis states carry most of the probability mass and a full 2<sup>n</sup> state-vector simulation becomes impractical, **qstvec** can simulate larger circuits by storing only the most relevant amplitudes.

## Installation

To install **qstvec** together with its dependencies:

```
pip install qstvec
```

Requirements:
* NumPy and Qiskit are installed automatically when you `pip install qstvec`.
* CuPy is optional and only needed if you want to use the GPU backend.  
(To install CuPy, please refer to the official [instructions](https://docs.cupy.dev/en/stable/install.html).)

After installation, `from qstvec import Statevector` should work in any Python environment.

## Basic usage

After installation, you can import `Statevector` from the package:

```python
from qstvec import Statevector

sv = Statevector(n_qubits=2) 

U = [[0, 1], [1, 0]]
qargs = [0]

sv.evolve(U, qargs)

sv.truncate(top_k=0, p_frac=1.0)  # no truncation, actually

print(sv.bit_string())  # prints the most probable bit string '01'
```

If you have a GPU and CuPy installed, you might want to try the GPU backend. (It should be faster, but more limited in terms of memory.) For this purpose, import `Statevector` from the GPU package:

```python
from qstvec_gpu import Statevector
```

## Examples

In the examples, we use some circuits from BlueQubit's [*Peaked Portal*](https://app.bluequbit.io/hackathons) hackathon.

### Little peak

The circuit `little_peak.qasm` corresponds to BlueQubit's *Problem 1: Little Peak*.

The Python script `little_peak.py` illustrates how to read the circuit and evolve the state vector, instruction by instruction, without truncation.

At the end, it prints the most probable bit string.

### Sharp peak

The circuit `sharp_peak.qasm` corresponds to BlueQubit's *Problem 3: Sharp Peak*.

The Python script `sharp_peak.py` implements the circuit simulation strategy described in the paper [1]. (Basically, it is a block-based simulation strategy where the gates in a block are composed into a single unitary, and the state vector is evolved block-by-block rather than instruction-by-instruction.)

To use this script, specify the *k* for top-*k* truncation and/or the *p* for *p*-mass truncation (top‑*k* keeps only the *k* largest‑probability basis states; *p*‑mass keeps enough terms to cover a fraction *p* of total probability). The default values *k*=0 and *p*=1.0 mean no truncation.

For example:

- `python sharp_peak.py 0 0.99` runs a simulation with a 99% fraction of the probability mass.
- `python sharp_peak.py 2**18 1.0` runs a simulation with a 2<sup>18</sup> limit on the number of terms.

### Test gates

This example ensures that the results are consistent with a state vector simulation based on [Qiskit](https://github.com/Qiskit/qiskit).

For this purpose, `test_gates.qasm` contains an example with all the standard gates available in OpenQASM 2.0 ([qelib1.inc](https://github.com/Qiskit/qiskit/blob/main/qiskit/qasm/libs/qelib1.inc)).

The Python script `test_gates.py` evolves a Qiskit `Statevector` and a qstvec `Statevector` side-by-side, and checks that the bit strings and probabilities agree after each circuit instruction.

## How to cite

If you find this package useful, please cite the paper:

[1] Diogo R. Ferreira, *A Sparse and Truncated State Vector Simulator for Peaked Circuits*, 7th IEEE International Conference on Quantum Computing and Engineering (QCE26), 2026.