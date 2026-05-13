# qstvec

**qstvec** is a Python code for approximate simulation of quantum circuits based on a sparse and truncated state vector representation.

It was originally developed for peaked circuits, where the goal is to find the most probable output bit string.

## Installation (development)

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/DiogoRibeiroFerreira/qstvec.git
cd qstvec
pip install -e .
```

This makes `qstvec` importable from any script in your environment while you work on the code.

Requirements:

- [NumPy](https://github.com/numpy/numpy) (installed automatically if declared as a dependency later, or install manually for now)
- [CuPy](https://github.com/cupy/cupy) is optional and only needed if you want to use the GPU backend.

## Basic usage

After installation, you can import `Statevector` from the package:

```python
from qstvec import Statevector

sv = Statevector(n_qubits=10)
# evolve sv instruction-by-instruction or block-by-block, with optional truncation
```

If you have a GPU and CuPy installed and want to experiment with the GPU backend (API still evolving), you can import from the GPU package:

```python
from qstvec_gpu import Statevector
```

In both cases, you instantiate the `Statevector` class and evolve the state vector instruction-by-instruction (or block-by-block), truncating the state vector at each step.

## Examples

In these examples, we use some circuits from BlueQubit's [*Peaked Portal*](https://app.bluequbit.io/hackathons) hackathon.

All example scripts live in the `examples/` directory and assume that `qstvec` has been installed (for example with `pip install -e .`).

### Little peak

The circuit `examples/little_peak.qasm` corresponds to BlueQubit's *Problem 1: Little Peak*.

The Python script `examples/little_peak.py` illustrates how to read the circuit and evolve the state vector, instruction by instruction, without any truncation.

At the end, it prints the most probable bit string.

### Sharp peak

The circuit `examples/sharp_peak.qasm` corresponds to BlueQubit's *Problem 3: Sharp Peak*.

The Python script `examples/sharp_peak.py` implements the circuit simulation strategy described in the paper [1]. Basically, it is a block-based simulation strategy where the gates in a block are composed into a single unitary, and the state vector is evolved block-by-block rather than instruction-by-instruction.

To use this script, specify the *k* for top-*k* truncation and/or the *p* for *p*-mass truncation. (The default values *k* = 0 and *p* = 1.0 mean no truncation.)

For example:

- `python examples/sharp_peak.py 0 0.99` runs a simulation with a 99% fraction of the probability mass.
- `python examples/sharp_peak.py 2**18 1.0` runs a simulation with a 2<sup>18</sup> limit on the number of terms.

### Test gates

This example ensures that the results are fully consistent with a state vector simulation based on [Qiskit](https://github.com/Qiskit/qiskit).

For this purpose, `examples/test_gates.qasm` contains an example with all the standard gates available in OpenQASM 2.0 ([qelib1.inc](https://github.com/Qiskit/qiskit/blob/main/qiskit/qasm/libs/qelib1.inc)).

The Python script `examples/test_gates.py` evolves a Qiskit `Statevector` and a qstvec `Statevector` side-by-side, and checks that the bit strings and probabilities agree after each circuit instruction.

## How to cite

If you find this code useful, please cite the paper:

[1] Diogo R. Ferreira, *A Sparse and Truncated State Vector Simulator for Peaked Circuits*, 7th IEEE International Conference on Quantum Computing and Engineering (QCE26), 2026.