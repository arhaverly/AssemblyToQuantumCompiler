# This project was created as part of Andy Haverly's PhD Dissertation. Please forgive the messiness :)


How can I use these transformations more easily?

Can I reuse registers? No. To maintain coherence, the reset gate cannot be used.

Desire:
Give the assembly program, get the circuit out.


How can I do this?
This is easier if the assembly program:
1. Does not reuse registers
2. Does not have branches
3. Only uses operations with a transformation


If it does reuse registers (almost every program does)
We can track where the register is in the qubits

What to do with flags?
We cannot use reset
This means that each flag is one time use
In assembly the flags are overwritten
This means that we can have a similar counter that we do for ancilla qubits


What about classical memory?
We should track the classical memory too



Implementing Grover's Algorithm
Added gates:
    HAD: applies the Hadamard gate to each qubit in the register
    XXX: applies the Pauli X gate to each qubit in the register
    TGT: Creates the target qubit, puts it in the |-> state, then applies cnot from the Rd[0] bit
    MCT: Creates the target qubit, puts it in the |-> state, then applies MCT from Rd
    DIF: Applies the diffuser to the registers listed

We want to know where the oracle is and what the reverse of it is.
