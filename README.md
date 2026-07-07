# qstvec

**qstvec** is a Python package for approximate simulation of quantum circuits based on a sparse and truncated state vector representation.

It was originally developed for _peaked circuits_, where the goal is to find the most probable bit string at the output of the circuit.

When only a small fraction of basis states carry most of the probability mass, and a full 2<sup>n</sup> state-vector simulation becomes unfeasible, **qstvec** can simulate large circuits by storing only the most relevant amplitudes.

## Installation

To install **qstvec**, you can use:

```
pip install qstvec
```

Requirements:
* The main requirements are NumPy and Qiskit.
* CuPy is optional and only needed if you want to use the GPU backend. In this case, please refer to the official [instructions](https://docs.cupy.dev/en/stable/install.html#installing-cupy) on how to install CuPy.

After installation, `from qstvec import Statevector` should work in any Python environment. 

For the GPU backend, use `from qstvec_gpu import Statevector` instead.

## Usage

After installation, you can import `Statevector` from the package:

```python
from qstvec import Statevector

# state vector for a 2-qubit system, initialized with |00>
sv = Statevector(n_qubits=2)

# unitary for a quantum NOT (Pauli-X) gate on single qubit
U = [[0, 1], [1, 0]]

# the unitary will be applied to the least-significant qubit
qargs = [0]                       

# evolve the state vector by applying the unitary
sv.evolve(U, qargs)

# optionally truncate (no effect in this example)
sv.truncate(top_k=0, p_frac=1.0)

# print the most probable bit string, i.e. '01'
print(sv.bit_string())
```

### GPU backend

If you have a GPU device and CuPy installed (as described in the CuPy [documentation](https://docs.cupy.dev/en/stable/install.html#requirements)), you might want to try the GPU backend. (It should be faster, but more limited in terms of memory.)

For this purpose, import `Statevector` from the GPU package instead:

```python
from qstvec_gpu import Statevector
```

## Examples

In the examples, we use some circuits from BlueQubit's [*Peaked Portal*](https://app.bluequbit.io/hackathons/oEOtLSSrPSVH60Ah) hackathon.

### Little peak

The circuit `little_peak.qasm` corresponds to BlueQubit's *Problem 1: Little Peak*.

The Python script `little_peak.py` illustrates how to read the circuit and evolve the state vector, instruction by instruction, without truncation.

At the end, it prints the most probable bit string.

### Sharp peak

The circuit `sharp_peak.qasm` corresponds to BlueQubit's *Problem 3: Sharp Peak*.

The Python script `sharp_peak.py` implements the circuit simulation strategy described in the paper [1]. (Basically, it is a block-based simulation strategy where multiple gates are composed into a single unitary, and the state vector is evolved block-by-block rather than instruction-by-instruction.)

To use this script, specify the *k* for top-*k* truncation and/or the *p* for *p*-mass truncation. (Top‑*k* truncation keeps only the *k* largest‑probability basis states, while *p*‑mass truncation keeps enough terms to cover a fraction *p* of the total probability mass). The default values are *k*=0 and *p*=1.0, which mean no truncation.

Examples:
* `python sharp_peak.py 0 0.99` runs a simulation with a 99% fraction of the total probability mass.
* `python sharp_peak.py 2**18 1.0` runs a simulation with a 2<sup>18</sup> upper limit on the number of terms.

### Test gates

This example shows that the results are consistent with a state vector simulation based on [Qiskit](https://github.com/Qiskit/qiskit).

For this purpose, `test_gates.qasm` contains examples of all the standard gates available in OpenQASM 2.0 (as specified in [qelib1.inc](https://github.com/Qiskit/qiskit/blob/main/qiskit/qasm/libs/qelib1.inc)).

The Python script `test_gates.py` evolves a `qiskit.Statevector` and a `qstvec.Statevector` side-by-side, and checks that the bit strings and probabilities agree after each circuit instruction.

## How to cite

If you find this package useful, please cite:

[1] Diogo R. Ferreira, *A Sparse and Truncated State Vector Simulator for Peaked Circuits*, 2026 (to appear)