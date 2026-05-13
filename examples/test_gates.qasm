OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

// --- 1-qubit parameterized gates ---
u3(0.1, 0.2, 0.3) q[0];
u2(0.1, 0.2)      q[1];
u1(0.3)           q[2];
u(0.4, 0.5, 0.6)  q[3];
p(0.7)            q[4];
rx(0.8)           q[5];
ry(0.9)           q[6];
rz(1.0)           q[7];

// --- 1-qubit Clifford/Pauli and related ---
id  q[0];
u0(0.0) q[1];
x   q[2];
y   q[3];
z   q[4];
h   q[5];
s   q[6];
sdg q[7];
t   q[0];
tdg q[1];
sx  q[2];
sxdg q[3];

// --- 2-qubit controlled gates (all orderings of two distinct qubits) ---
cx q[0], q[1];
cx q[1], q[0];

cz q[0], q[1];
cz q[1], q[0];

cy q[0], q[1];
cy q[1], q[0];

ch q[0], q[1];
ch q[1], q[0];

crx(0.2) q[0], q[1];
crx(0.2) q[1], q[0];

cry(0.3) q[0], q[1];
cry(0.3) q[1], q[0];

crz(0.4) q[0], q[1];
crz(0.4) q[1], q[0];

cu1(0.5) q[0], q[1];
cu1(0.5) q[1], q[0];

cp(0.6) q[0], q[1];
cp(0.6) q[1], q[0];

cu3(0.7, 0.8, 0.9) q[0], q[1];
cu3(0.7, 0.8, 0.9) q[1], q[0];

cu(1.0, 1.1, 1.2, 1.3) q[0], q[1];
cu(1.0, 1.1, 1.2, 1.3) q[1], q[0];

csx q[0], q[1];
csx q[1], q[0];

// --- 2-qubit symmetric gates (include both orders anyway) ---
swap q[0], q[1];
swap q[1], q[0];

rxx(0.2) q[0], q[1];
rxx(0.2) q[1], q[0];

rzz(0.3) q[0], q[1];
rzz(0.3) q[1], q[0];

// --- 3-qubit gates (several distinct orderings) ---
// ccx (Toffoli)
ccx q[0], q[1], q[2];
ccx q[0], q[2], q[1];
ccx q[1], q[0], q[2];
ccx q[1], q[2], q[0];
ccx q[2], q[0], q[1];
ccx q[2], q[1], q[0];

// cswap (Fredkin): control, target1, target2
cswap q[0], q[1], q[2];
cswap q[0], q[2], q[1];
cswap q[1], q[0], q[2];
cswap q[1], q[2], q[0];
cswap q[2], q[0], q[1];
cswap q[2], q[1], q[0];

// rccx (relative-phase CCX)
rccx q[0], q[1], q[2];
rccx q[0], q[2], q[1];
rccx q[1], q[0], q[2];
rccx q[1], q[2], q[0];
rccx q[2], q[0], q[1];
rccx q[2], q[1], q[0];

// rc3x (relative-phase 3-controlled X)
// convention: controls, ..., target (last argument)
rc3x q[0], q[1], q[2], q[3];
rc3x q[0], q[1], q[3], q[2];
rc3x q[0], q[2], q[1], q[3];
rc3x q[1], q[0], q[2], q[3];

// c3x (3-controlled X)
c3x q[0], q[1], q[2], q[3];
c3x q[0], q[1], q[3], q[2];
c3x q[0], q[2], q[1], q[3];
c3x q[1], q[0], q[2], q[3];

// c3sqrtx (3-controlled SX)
c3sqrtx q[0], q[1], q[2], q[3];
c3sqrtx q[0], q[1], q[3], q[2];
c3sqrtx q[0], q[2], q[1], q[3];
c3sqrtx q[1], q[0], q[2], q[3];

// c4x (4-controlled X)
c4x q[0], q[1], q[2], q[3], q[4];
c4x q[0], q[1], q[3], q[2], q[4];
c4x q[1], q[0], q[2], q[3], q[4];
c4x q[1], q[2], q[3], q[0], q[4];