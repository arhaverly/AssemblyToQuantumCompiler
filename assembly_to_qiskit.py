'''
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


Branching
B: Precompiler classically unravel the loop (TODO)

BEQ, BNE: Might be possible to classically unravel the loop
    Easy: If it's a FOR loop, just unravel the set number of times

    Difficult: If the condition is difficult to predict, we can use controlled gates, 
        but then need to carry down the registers if the value is not set.
        We can carry down the registers by using controlled gates too.
'''

#initialization
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

import json
import random
import sys
import io


# Redirect standard error
original_stderr = sys.stderr
sys.stderr = io.StringIO()

# importing Qiskit
from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.providers.ibmq import least_busy
from qiskit.circuit.library import IntegerComparator
from qiskit.providers.aer import QasmSimulator

from qiskit.circuit.library import MCMT, CSwapGate, CHGate

# import basic plot tools
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

# Restore standard error
sys.stderr = original_stderr



allowed_operations = {
    'ADC',
    'ADD',
    'AND',
    'BIC',
    'CMN',
    'CMP',
    'EOR',
    'LSL',
    'LSR',
    'MLA',
    'MOV',
    'MRS',
    'MSR',
    'MUL',
    'MVN',
    'ORR',
    'RSB',
    'RSC',
    'SBC',
    'STR',
    'SUB',
    'TEQ',
    'TST',
    'HAD',
    'XXX',
    'DIF',
    'TGT',
    'MCT',
    'BAR'
}

first_target = True


# TODO: create a precompiler that unravels branches
def precompile(filename):
    pass



def qor():
    qc = QuantumCircuit(3)

    qc.x(0)
    qc.x(1)

    qc.ccx(0,1,2)
    qc.x(0)
    qc.x(1)
    qc.x(2)

    QOR = qc.to_gate()
    QOR.name = 'M_QOR'
    return QOR


def full_adder(qc, A, B, Cin, Sum, Cout):
    qc.barrier()
    qc.cx(A, Sum)
    qc.cx(B, Sum)

    if Cin != None:
        qc.cx(Cin, Sum)

    if Cout != None:
        qc.mct([A, B], Cout)

        if Cin != None:
            qc.mct([A, Cin], Cout)
            qc.mct([B, Cin], Cout)




def ripple_carry_adder(qc, register_size, Rd, Rn, Operand, CarryRegister, CarryFlag):
    full_adder(qc, Rn[0], Operand[0], None, Rd[0], CarryRegister[0])
    qc.barrier()

    for i in range(register_size-2):
        full_adder(qc, Rn[i+1], Operand[i+1], CarryRegister[i], Rd[i+1], CarryRegister[i+1])

    if CarryFlag != None:
        full_adder(qc, Rn[register_size-1], Operand[register_size-1], CarryRegister[register_size-2], Rd[register_size-1], CarryFlag)
    else:
        full_adder(qc, Rn[register_size-1], Operand[register_size-1], CarryRegister[register_size-2], Rd[register_size-1], None)
    qc.barrier()



def int_to_binary_string(num, register_size):
    # Convert to binary without '0b' prefix and pad with zeroes if needed
    binary_str = format(num, 'b').zfill(register_size)

    # If the binary string is longer than the register size, take the last 'register_size' bits
    return binary_str[-register_size:]


def get_register_location(register_name, register_size, additional_flags):
    register = int(register_name.replace('R', ''))

    return [i for i in range(register*register_size + additional_flags, (register+1)*register_size + additional_flags)]

def get_classical_register_location(register_size, register_name):
    register = int(register_name.replace('CR', ''))

    return [i for i in range(register*register_size, (register+1)*register_size)]

def get_target_location(register_size):
    return 0


def write_immediate(qc, register_size, Rm, immediate):
    binary_string = int_to_binary_string(int(immediate.replace('#', '')), register_size)
    for i in range(register_size):
        if binary_string[register_size - i - 1] == '1':
            qc.x(Rm[i])


def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits): # depth += 1
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits): # depth += 1
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits-1) # depth += 1
    qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli  # depth += 1
    qc.h(nqubits-1) # depth += 1
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits): # depth += 1
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits): # depth += 1
        qc.h(qubit)
    # We will return the diffuser as a gate
    U_s = qc.to_gate()
    U_s.name = 'DIF'
    return U_s


def ADC(qc, register_size, ancilla_counter, additional_flags, carry_flag_counter, carry_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)

    if '#' in op3:
        Rm = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(op3.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Rm[i])
    else:
        Rm = get_register_location(op3, register_size, additional_flags)


    CarryRegister = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    print('Rd:', Rd)
    print('Rn:', Rn)
    print('Op2:', Op2)
    print('CarryRegister:', CarryRegister)


    ripple_carry_adder(qc, register_size, Rd, Rn, Op2, CarryRegister, carry_flags[carry_flag_counter])

    return ancilla_counter





def ADD(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)

    if '#' in op3:
        Rm = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(op3.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Rm[i])
    else:
        Rm = get_register_location(op3, register_size, additional_flags)

    print('Rd:', Rd)
    print('Rn:', Rn)
    print('Rm:', Rm)


    ripple_carry_adder(qc, register_size, Rd, Rn, Rm, [i for i in range(ancilla_counter, ancilla_counter + register_size-1)], None)

    ancilla_counter += register_size - 1

    return ancilla_counter


def AND(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)

    if '#' in op3:
        Op2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size
        write_immediate(qc, register_size, Op2, op3)
    else:
        Op2 = get_register_location(op3, register_size, additional_flags)

    print('Rd:', Rd)
    print('Rn:', Rn)
    print('Op2:', Op2)




    qc.mct([Rn, Op2], Rd)


    return ancilla_counter



def BIC(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)

    if '#' in op3:
        Op2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(op3.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Op2[i])
    else:
        Op2 = get_register_location(op3, register_size, additional_flags)



    print('Rd:', Rd)
    print('Rn:', Rn)
    print('Op2:', Op2)


    qc.x(Op2)
    qc.mct([Rn, Op2], Rd)

    return ancilla_counter


def CMN(qc, register_size, ancilla_counter, additional_flags, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags, Rn, Op2):
    Rn = get_register_location(Rn, register_size, additional_flags)

    if '#' in Op2:
        Rm = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(Op2.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Rm[i])
    else:
        Rm = get_register_location(Op2, register_size, additional_flags)


    CarryRegister = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    OverflowAncRegister = [i for i in range(ancilla_counter, ancilla_counter + 2)]
    ancilla_counter += 2

    Rd = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    print('Rn:', Rn)
    print('Rm:', Rm)
    print('CarryRegister:', CarryRegister)
    print('OverflowAncRegister:', OverflowAncRegister)
    print('Rd:', Rd)





    ripple_carry_adder(qc, register_size, Rd, Rn, Rm, CarryRegister, carry_flags[carry_flag_counter])

    # zero
    qc.barrier()
    qc.x(Rd)
    qc.mct(Rd, zero_flags[zero_flag_counter])
    qc.x(Rd)

    # negative
    qc.barrier()
    qc.cx(Rd[register_size-1], negative_flags[negative_flag_counter])

    # overflow
    # occurs when the two operands have the same sign (both positive or both negative), but the result has a different sign
    qc.barrier()
    qc.x(Rn[register_size-1])
    qc.x(Rm[register_size-1])
    qc.mct([Rn[register_size-1], Rm[register_size-1], Rd[register_size-1]], OverflowAncRegister[0])
    qc.x(Rn[register_size-1])
    qc.x(Rm[register_size-1])

    qc.x(Rd[register_size-1])
    qc.mct([Rn[register_size-1], Rm[register_size-1], Rd[register_size-1]], OverflowAncRegister[1])
    qc.x(Rd[register_size-1])

    qc.append(qor(), [OverflowAncRegister[0], OverflowAncRegister[1], overflow_flags[overflow_flag_counter]])
    qc.barrier()

    return ancilla_counter



def CMP(qc, register_size, ancilla_counter, additional_flags, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags, Rn, Op2):
    Rn = get_register_location(Rn, register_size, additional_flags)

    if '#' in Op2:
        Rm = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size
        write_immediate(qc, register_size, Rm, Op2)
    else:
        Rm = get_register_location(Op2, register_size, additional_flags)

    AdditionAncRegister = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    NegatedOp2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    CarryRegister0 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    CarryRegister1 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    OverflowAncRegister = [i for i in range(ancilla_counter, ancilla_counter + 2)]
    ancilla_counter += 2

    Rd = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    print('Rn:', Rn)
    print('Rm:', Rm)
    print('AdditionAncRegister:', AdditionAncRegister)
    print('NegatedOp2:', NegatedOp2)
    print('CarryRegister0:', CarryRegister0)
    print('CarryRegister1:', CarryRegister1)
    print('OverflowAncRegister:', OverflowAncRegister)
    print('Rd:', Rd)

    



    # take the twos complement of Op2 (invert and add 1)
    qc.barrier()
    qc.x(AdditionAncRegister[0])
    qc.x(Rm)
    ripple_carry_adder(qc, register_size, NegatedOp2, AdditionAncRegister, Rm, CarryRegister0, None)
    qc.barrier()


    ripple_carry_adder(qc, register_size, Rd, Rn, NegatedOp2, CarryRegister1, carry_flags[carry_flag_counter])

    # zero
    qc.barrier()
    qc.x(Rd)
    qc.mct(Rd, zero_flags[zero_flag_counter])
    qc.x(Rd)

    # negative
    qc.barrier()
    qc.cx(Rd[register_size-1], negative_flags[negative_flag_counter])


    # overflow
    # occurs when the two operands have the same sign (both positive or both negative), but the result has a different sign
    qc.barrier()
    qc.x(Rn[register_size-1])
    qc.x(NegatedOp2[register_size-1])
    qc.mct([Rn[register_size-1], NegatedOp2[register_size-1], Rd[register_size-1]], OverflowAncRegister[0])
    qc.x(Rn[register_size-1])
    qc.x(NegatedOp2[register_size-1])

    qc.x(Rd[register_size-1])
    qc.mct([Rn[register_size-1], NegatedOp2[register_size-1], Rd[register_size-1]], OverflowAncRegister[1])
    qc.x(Rd[register_size-1])

    qc.append(qor(), [OverflowAncRegister[0], OverflowAncRegister[1], overflow_flags[overflow_flag_counter]])
    qc.barrier()

    return ancilla_counter





def EOR(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)
    
    if '#' in op3:
        Op2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(op3.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Op2[i])
    else:
        Op2 = get_register_location(op3, register_size, additional_flags)

    RnAndNotOp2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    Op2AndNotRn = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size



    qc.x(Op2)
    qc.mct([Rn, Op2], RnAndNotOp2)
    qc.x(Op2)

    qc.barrier()

    qc.x(Rn)
    qc.mct([Rn, Op2], Op2AndNotRn)
    qc.x(Rn)

    qc.barrier()

    qc.append(qor(), [RnAndNotOp2, Op2AndNotRn, Rd])

    return ancilla_counter





def HAD(qc, register_size, additional_flags, op1):
    Rd = get_register_location(op1, register_size, additional_flags)

    qc.h(Rd)


def XXX(qc, register_size, additional_flags, op1):
    Rd = get_register_location(op1, register_size, additional_flags)

    qc.x(Rd)

def TGT(qc, register_size, additional_flags, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags, op1):
    target = get_target_location(register_size)

    global first_target

    if first_target:
        qc.x(target)
        qc.h(target)
        first_target = False


    if op1 == 'ZERO':
        # qc.x(zero_flags[zero_flag_counter])
        qc.cx(zero_flags[zero_flag_counter], target)
        # qc.x(zero_flags[zero_flag_counter])
    elif op1 == 'NEGATIVE':
        qc.cx(negative_flags[negative_flag_counter], target)
    elif op1 == 'CARRY':
        qc.cx(carry_flags[carry_flag_counter], target)
    elif op1 == 'OVERFLOW':
        qc.cx(overflow_flags[overflow_flag_counter], target)
    else:
        Rd = get_register_location(op1, register_size, additional_flags)
        qc.cx(Rd[0], target)


def BAR(qc):
    qc.barrier()


def MCT(qc, register_size, additional_flags, op1):
    Rd = get_register_location(op1, register_size, additional_flags)
    target = get_target_location(register_size)

    qc.x(target)
    qc.h(target)

    qc.mct(Rd, target)



def DIF(qc, register_size, additional_flags, rlist):
    qubits = []
    print(rlist)
    for register in rlist:
        qubits.extend(get_register_location(register.replace('{','').replace('}',''), register_size, additional_flags))

    # qubits.append(0)

    print(qubits)

    qc.append(diffuser(len(qubits)), qubits)




# the immediate value is classically determined and put into the swap gates
# TODO: if needed to conditionally control the amount of shifting, turn into a one-hot encoded and shift off of that single control
def LSL(qc, register_size, additional_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)

    print('Rd:', Rd)
    print('Rn:', Rn)
    shift = int(op3.replace('#',''))

    # if shifted 1, Rd[5] gets Rn[4]
    # 2: Rd[5] gets Rn[3], Rd[4] gets Rn[2]
    for i in range(register_size - shift):
        print(i)
        print(register_size - i - shift)
        qc.swap(Rd[register_size - 1 - i], Rn[register_size - 1 - i - shift])


# the immediate value is classically determined and put into the swap gates
# TODO: if needed to conditionally control the amount of shifting, turn into a one-hot encoded and shift off of that single control
def LSR(qc, register_size, additional_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)

    print('Rd:', Rd)
    print('Rn:', Rn)
    shift = int(op3.replace('#',''))

    # if shifted 1, Rd[0] gets Rn[1]
    # 2: Rd[0] gets Rn[2], Rd[1] gets Rn[3]
    for i in range(register_size - shift):
        qc.swap(Rd[i], Rn[i + shift])


# TODO need to generalize it. yikes...
def MLA(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3, op4):
    if register_size != 4:
        raise Exception('MLA is only implemented for 4 bit registers right now, with only the 2 LSB being multiplied')

    Rd = get_register_location(op1, register_size, additional_flags)
    Rm = get_register_location(op2, register_size, additional_flags)
    Rs = get_register_location(op3, register_size, additional_flags)
    Rn = get_register_location(op4, register_size, additional_flags)

    Ancilla = [i for i in range(ancilla_counter, ancilla_counter + 7)]
    ancilla_counter += 7

    MUL_Result = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    print('Rd:', Rd)
    print('Rm:', Rm)
    print('Rs:', Rs)
    print('Ancilla:', Ancilla)
    print('MUL_Result:', MUL_Result)

    # R0
    qc.mct([Rm[0], Rs[0]], MUL_Result[0])

    qc.barrier()

    # R1
    qc.mct([Rm[0], Rs[1]], Ancilla[0])
    qc.mct([Rm[1], Rs[0]], Ancilla[1])

    full_adder(qc, Ancilla[0], Ancilla[1], None, MUL_Result[1], Ancilla[2])

    qc.barrier()

    # R2, R3
    qc.mct([Rm[1], Rs[1]], Ancilla[3])
    full_adder(qc, Ancilla[2], Ancilla[3], None, MUL_Result[2], MUL_Result[3])

    # add Rn
    qc.barrier()
    full_adder(qc, MUL_Result[0], Rn[0], None, Rd[0], Ancilla[4])
    full_adder(qc, MUL_Result[1], Rn[1], Ancilla[4], Rd[1], Ancilla[5])
    full_adder(qc, MUL_Result[2], Ancilla[5], None, Rd[2], Ancilla[6])
    full_adder(qc, MUL_Result[3], Ancilla[6], None, Rd[3], None)

    return ancilla_counter




def MOV(qc, register_size, additional_flags, op1, op2):
    Rd = get_register_location(op1, register_size, additional_flags)
    print('Rd:', Rd)

    if '#' in op2:
        binary_string = int_to_binary_string(int(op2.replace('#', '')), register_size)
        print(binary_string)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Rd[i])




def MRS(qc, register_size, additional_flags, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags, Rn):
    Rn = get_register_location(Rn, register_size, additional_flags)

    qc.cx(zero_flags[zero_flag_counter], Rn[0])
    qc.cx(negative_flags[negative_flag_counter], Rn[1])
    qc.cx(carry_flags[carry_flag_counter], Rn[2])
    qc.cx(overflow_flags[overflow_flag_counter], Rn[3])





def MSR(qc, register_size, additional_flags, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags, Rn):
    Rn = get_register_location(Rn, register_size, additional_flags)

    qc.cx(Rn[0], zero_flags[zero_flag_counter])
    qc.cx(Rn[1], negative_flags[negative_flag_counter])
    qc.cx(Rn[2], carry_flags[carry_flag_counter])
    qc.cx(Rn[3], overflow_flags[overflow_flag_counter])



# TODO need to generalize it. yikes...
def MUL(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3):
    if register_size != 4:
        raise Exception('MUL is only implemented for 4 bit registers right now, with only the 2 LSB being multiplied')

    Rd = get_register_location(op1, register_size, additional_flags)
    Rm = get_register_location(op2, register_size, additional_flags)
    Rs = get_register_location(op3, register_size, additional_flags)

    Ancilla = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    print('Rd:', Rd)
    print('Rm:', Rm)
    print('Rs:', Rs)
    print('Ancilla:', Ancilla)

    # R0
    qc.mct([Rm[0], Rs[0]], Rd[0])

    qc.barrier()

    # R1
    qc.mct([Rm[0], Rs[1]], Ancilla[0])
    qc.mct([Rm[1], Rs[0]], Ancilla[1])

    full_adder(qc, Ancilla[0], Ancilla[1], None, Rd[1], Ancilla[2])

    qc.barrier()

    # R2, R3
    qc.mct([Rm[1], Rs[1]], Ancilla[3])
    full_adder(qc, Ancilla[2], Ancilla[3], None, Rd[2], Rd[3])


    return ancilla_counter


def MOV(qc, register_size, additional_flags, op1, op2):
    Rd = get_register_location(op1, register_size, additional_flags)
    print('Rd:', Rd)

    if '#' in op2:
        binary_string = int_to_binary_string(int(op2.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Rd[i])
    else:
        Rn = get_register_location(op2, register_size, additional_flags)
        for i in range(register_size):
            qc.cnot(Rn[i], Rd[i])


def MVN(qc, register_size, additional_flags, op1, op2):
    Rd = get_register_location(op1, register_size, additional_flags)
    print('Rd:', Rd)

    if '#' in op2:
        binary_string = int_to_binary_string(int(op2.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '0':
                qc.x(Rd[i])
    else:
        Rn = get_register_location(op2, register_size, additional_flags)
        for i in range(register_size):
            qc.x(Rd[i])
            qc.cnot(Rn[i], Rd[i])


def ORR(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)

    if '#' in op3:
        Op2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(op3.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Op2[i])
    else:
        Op2 = get_register_location(op3, register_size, additional_flags)


    print('Rd:', Rd)
    print('Rn:', Rn)
    print('Op2:', Op2)

    qc.x(Rn)
    qc.x(Op2)
    qc.ccx(Rn, Op2, Rd)
    qc.x(Rn)
    qc.x(Op2)
    qc.x(Rd)

    return ancilla_counter



# Rd := Op2 - Rn
def RSB(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)

    if '#' in op3:
        Op2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(op3.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Op2[i])
    else:
        Op2 = get_register_location(op3, register_size, additional_flags)


    AdditionAncRegister = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    NegatedRn = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    CarryRegister0 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    CarryRegister1 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1


    print('Rn:', Rn)
    print('Op2:', Op2)
    print('AdditionAncRegister:', AdditionAncRegister)
    print('NegatedRn:', NegatedRn)
    print('CarryRegister0:', CarryRegister0)
    print('CarryRegister1:', CarryRegister1)
    print('Rd:', Rd)




    # take the twos complement of Op2 (invert and add 1)
    qc.barrier()
    qc.x(AdditionAncRegister[0])
    qc.x(Rn)
    ripple_carry_adder(qc, register_size, NegatedRn, AdditionAncRegister, Rn, CarryRegister0, None)
    qc.barrier()


    ripple_carry_adder(qc, register_size, Rd, Op2, NegatedRn, CarryRegister1, None)

    return ancilla_counter




# Rd := Op2 - Rn + Carry - 1
def RSC(qc, register_size, ancilla_counter, additional_flags, carry_flag_counter, carry_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)
    
    if '#' in op3:
        Op2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(op3.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Op2[i])
    else:
        Op2 = get_register_location(op3, register_size, additional_flags)



    Negative1 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    AdditionAncRegister = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    Op2MinusRn = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    CarryMinus1 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    NegatedRn = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    CarryFlag = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    CarryRegister0 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    CarryRegister1 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    CarryRegister2 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    CarryRegister3 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1
    


    print('Rd:', Rd)
    print('Rn:', Rn)
    print('Op2:', Op2)
    print('Negative1:', Negative1)
    print('AdditionAncRegister:', AdditionAncRegister)
    print('Op2MinusRn:', Op2MinusRn)
    print('CarryMinus1:', CarryMinus1)
    print('NegatedRn:', NegatedRn)
    print('CarryFlag:', CarryFlag)
    print('CarryRegister0:', CarryRegister0)
    print('CarryRegister1:', CarryRegister1)
    print('CarryRegister2:', CarryRegister2)
    print('CarryRegister3:', CarryRegister3)



    # take the twos complement of Rn (invert and add 1)
    qc.x(AdditionAncRegister[0])
    qc.x(Rn)
    ripple_carry_adder(qc, register_size, NegatedRn, AdditionAncRegister, Rn, CarryRegister0, None)
    qc.barrier()

    # add the Op2 and NegatedRn
    ripple_carry_adder(qc, register_size, Op2MinusRn, Op2, NegatedRn, CarryRegister1, None)

    # carry - 1
    qc.x(Negative1)
    qc.cx(carry_flags[carry_flag_counter], CarryFlag[0])
    ripple_carry_adder(qc, register_size, CarryMinus1, CarryFlag, Negative1, CarryRegister2, None)


    # add CarryMinus1
    ripple_carry_adder(qc, register_size, Rd, CarryMinus1, Op2MinusRn, CarryRegister3, None)


    return ancilla_counter



# Rd := Rn - Op2 + (Carry - 1)
def SBC(qc, register_size, ancilla_counter, additional_flags, carry_flag_counter, carry_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)
    
    if '#' in op3:
        Op2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(op3.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Op2[i])
    else:
        Op2 = get_register_location(op3, register_size, additional_flags)

    Negative1 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    AdditionAncRegister = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    RnMinusOp2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    CarryMinus1 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    NegatedOp2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    CarryFlag = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    CarryRegister0 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    CarryRegister1 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    CarryRegister2 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    CarryRegister3 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1
    


    print('Rd:', Rd)
    print('Rn:', Rn)
    print('Op2:', Op2)
    print('Negative1:', Negative1)
    print('AdditionAncRegister:', AdditionAncRegister)
    print('RnMinusOp2:', RnMinusOp2)
    print('CarryMinus1:', CarryMinus1)
    print('NegatedOp2:', NegatedOp2)
    print('CarryFlag:', CarryFlag)
    print('CarryRegister0:', CarryRegister0)
    print('CarryRegister1:', CarryRegister1)
    print('CarryRegister2:', CarryRegister2)
    print('CarryRegister3:', CarryRegister3)



    # take the twos complement of Op2 (invert and add 1)
    qc.x(AdditionAncRegister[0])
    qc.x(Op2)
    ripple_carry_adder(qc, register_size, NegatedOp2, AdditionAncRegister, Op2, CarryRegister0, None)
    qc.barrier()

    # add Rn and NegatedOp2
    ripple_carry_adder(qc, register_size, RnMinusOp2, Rn, NegatedOp2, CarryRegister1, None)


    # get Carry - 1
    qc.x(Negative1)
    qc.cx(carry_flags[carry_flag_counter], CarryFlag[0])
    ripple_carry_adder(qc, register_size, CarryMinus1, CarryFlag, Negative1, CarryRegister2, None)

    # add CarryMinus1
    ripple_carry_adder(qc, register_size, Rd, RnMinusOp2, CarryMinus1, CarryRegister3, None)

    return ancilla_counter







def STR(qc, cr, register_size, additional_flags, op1, op2, op3):
    # need to add offset capability
    Rd = get_classical_register_location(register_size, op1)
    Rn = get_register_location(op2, register_size, additional_flags)

    print('Rd (classical):', Rd)
    print('Rn:', Rn)

    qc.measure(Rn, cr[Rd])




# Rd := Rn - Op2
def SUB(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3):
    Rd = get_register_location(op1, register_size, additional_flags)
    Rn = get_register_location(op2, register_size, additional_flags)

    if '#' in op3:
        Rm = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(op3.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Rm[i])
    else:
        Rm = get_register_location(op3, register_size, additional_flags)

    AdditionAncRegister = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    NegatedOp2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    CarryRegister0 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1

    CarryRegister1 = [i for i in range(ancilla_counter, ancilla_counter + register_size-1)]
    ancilla_counter += register_size-1


    print('Rn:', Rn)
    print('Rm:', Rm)
    print('AdditionAncRegister:', AdditionAncRegister)
    print('NegatedOp2:', NegatedOp2)
    print('CarryRegister0:', CarryRegister0)
    print('CarryRegister1:', CarryRegister1)
    print('Rd:', Rd)




    # take the twos complement of Op2 (invert and add 1)
    qc.barrier()
    qc.x(AdditionAncRegister[0])
    qc.x(Rm)
    ripple_carry_adder(qc, register_size, NegatedOp2, AdditionAncRegister, Rm, CarryRegister0, None)
    qc.barrier()


    ripple_carry_adder(qc, register_size, Rd, Rn, NegatedOp2, CarryRegister1, None)

    return ancilla_counter






# CPSR flags := Rn AND Op2
def TEQ(qc, register_size, ancilla_counter, additional_flags, zero_flag_counter, negative_flag_counter, overflow_flag_counter, zero_flags, negative_flags, overflow_flags, Rn, Op2):
    Rn = get_register_location(Rn, register_size, additional_flags)

    if '#' in Op2:
        Rm = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(Op2.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Rm[i])
    else:
        Rm = get_register_location(Op2, register_size, additional_flags)

    RnAndNotOp2 = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    Op2AndNotRn = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    OverflowAncRegister = [i for i in range(ancilla_counter, ancilla_counter + 2)]
    ancilla_counter += 2

    Rd = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    print('Rn:', Rn)
    print('Rm:', Rm)
    print('RnAndNotOp2:', RnAndNotOp2)
    print('Op2AndNotRn:', Op2AndNotRn)
    print('OverflowAncRegister:', OverflowAncRegister)
    print('Rd:', Rd)



    # EOR
    qc.x(Rm)
    qc.mct([Rn, Rm], RnAndNotOp2)
    qc.x(Rm)

    qc.barrier()

    qc.x(Rn)
    qc.mct([Rn, Rm], Op2AndNotRn)
    qc.x(Rn)

    qc.barrier()

    qc.append(qor(), [RnAndNotOp2, Op2AndNotRn, Rd])

    qc.barrier()



    # zero
    qc.barrier()
    qc.x(Rd)
    qc.mct(Rd, zero_flags[zero_flag_counter])
    qc.x(Rd)

    # negative
    qc.barrier()
    qc.cx(Rd[register_size-1], negative_flags[negative_flag_counter])

    # overflow
    # occurs when the two operands have the same sign (both positive or both negative), but the result has a different sign
    qc.barrier()
    qc.x(Rn[register_size-1])
    qc.x(Rm[register_size-1])
    qc.mct([Rn[register_size-1], Rm[register_size-1], Rd[register_size-1]], OverflowAncRegister[0])
    qc.x(Rn[register_size-1])
    qc.x(Rm[register_size-1])

    qc.x(Rd[register_size-1])
    qc.mct([Rn[register_size-1], Rm[register_size-1], Rd[register_size-1]], OverflowAncRegister[1])
    qc.x(Rd[register_size-1])

    qc.append(qor(), [OverflowAncRegister[0], OverflowAncRegister[1], overflow_flags[overflow_flag_counter]])
    qc.barrier()

    return ancilla_counter




# CPSR flags := Rn AND Op2
def TST(qc, register_size, ancilla_counter, additional_flags, zero_flag_counter, negative_flag_counter, overflow_flag_counter, zero_flags, negative_flags, overflow_flags, Rn, Op2):
    Rn = get_register_location(Rn, register_size, additional_flags)

    if '#' in Op2:
        Rm = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
        ancilla_counter += register_size

        binary_string = int_to_binary_string(int(Op2.replace('#', '')), register_size)
        for i in range(register_size):
            if binary_string[register_size - i - 1] == '1':
                qc.x(Rm[i])
    else:
        Rm = get_register_location(Op2, register_size, additional_flags)


    OverflowAncRegister = [i for i in range(ancilla_counter, ancilla_counter + 2)]
    ancilla_counter += 2

    Rd = [i for i in range(ancilla_counter, ancilla_counter + register_size)]
    ancilla_counter += register_size

    print('Rn:', Rn)
    print('Rm:', Rm)
    print('OverflowAncRegister:', OverflowAncRegister)
    print('Rd:', Rd)





    # AND
    qc.mct([Rn, Rm], Rd)


    # zero
    qc.barrier()
    qc.x(Rd)
    qc.mct(Rd, zero_flags[zero_flag_counter])
    # qc.x(Rd)

    # negative
    qc.barrier()
    qc.cx(Rd[register_size-1], negative_flags[negative_flag_counter])

    # overflow
    # occurs when the two operands have the same sign (both positive or both negative), but the result has a different sign
    qc.barrier()
    qc.x(Rn[register_size-1])
    qc.x(Rm[register_size-1])
    qc.mct([Rn[register_size-1], Rm[register_size-1], Rd[register_size-1]], OverflowAncRegister[0])
    qc.x(Rn[register_size-1])
    qc.x(Rm[register_size-1])

    qc.x(Rd[register_size-1])
    qc.mct([Rn[register_size-1], Rm[register_size-1], Rd[register_size-1]], OverflowAncRegister[1])
    qc.x(Rd[register_size-1])

    qc.append(qor(), [OverflowAncRegister[0], OverflowAncRegister[1], overflow_flags[overflow_flag_counter]])
    qc.barrier()

    return ancilla_counter





def get_instructions(assembly_program):
    instructions = []
    with open(assembly_program, 'r') as file:
        for line in file:
            stripped_line = line.split(';')[0].strip().replace(',', '')
            
            if stripped_line:
                tokens = stripped_line.split(' ')
                if '' in tokens:
                    tokens.remove('')

                if ' ' in tokens:
                    tokens.remove(' ')

                if '\t' in tokens:
                    tokens.remove('\t')

                instructions.append(tokens)

    return instructions


def add_ancilla(instruction, register_size):
    additional_ancilla = 0
    if instruction[0] == 'ADC':
        additional_ancilla += register_size - 1
        if '#' in instruction[3]:
            additional_ancilla += register_size
    elif instruction[0] == 'ADD':
        additional_ancilla += register_size - 1
        if '#' in instruction[3]:
            additional_ancilla += register_size
    elif instruction[0] in ['AND', 'BIC', 'ORR']:
        if '#' in instruction[3]:
            additional_ancilla += register_size
    elif instruction[0] == 'CMN':
        additional_ancilla += 2*register_size + 1
        if '#' in instruction[2]:
            additional_ancilla += register_size
    elif instruction[0] == 'CMP':
        additional_ancilla += 5*register_size
        if '#' in instruction[2]:
            additional_ancilla += register_size
    elif instruction[0] == 'EOR':
        additional_ancilla += 2*register_size
        if '#' in instruction[3]:
            additional_ancilla += register_size
    elif instruction[0] == 'MLA':
        additional_ancilla += register_size+7
    elif instruction[0] == 'MUL':
        additional_ancilla += register_size
    elif instruction[0] in ['SBC', 'RSC']:
        additional_ancilla = 10*register_size - 4
        if '#' in instruction[3]:
            additional_ancilla += register_size
    elif instruction[0] in ['RSB', 'SUB']:
        additional_ancilla += 4*register_size-2
        if '#' in instruction[3]:
            additional_ancilla += register_size
    elif instruction[0] == 'TEQ':
        additional_ancilla += 3*register_size + 2
        if '#' in instruction[2]:
            additional_ancilla += register_size
    elif instruction[0] == 'TST':
        additional_ancilla += register_size + 2
        if '#' in instruction[2]:
            additional_ancilla += register_size

    return additional_ancilla


def add_target(instruction):
    if instruction[0] in ['MCT', 'TGT']:
        return 1

    return 0


def add_zero(instruction):
    if instruction[0] in ['CMN', 'CMP', 'MSR', 'TEQ', 'TST']:
        return 1

    return 0


def add_negative(instruction):
    if instruction[0] in ['CMN', 'CMP', 'MSR', 'TEQ', 'TST']:
        return 1

    return 0


def add_carry(instruction):
    if instruction[0] in ['ADC', 'CMN', 'CMP', 'MSR', 'TEQ', 'TST']:
        return 1

    return 0


def add_overflow(instruction):
    if instruction[0] in ['CMN', 'CMP', 'MSR', 'TEQ', 'TST']:
        return 1

    return 0


def add_classical(instruction, register_size):
    additional_classical = 0
    if instruction[0] == 'STR':
        additional_classical += register_size

    return additional_classical


def initialize(instructions, register_size):
    highest_register = 0
    ancilla = 0
    targets = 0
    zero_flag = 0
    negative_flag = 0
    carry_flag = 0
    overflow_flag = 0
    classical_memory_needed = 0

    for i, instruction in enumerate(instructions):
        if i < 1:
            continue

        ancilla += add_ancilla(instruction, register_size)
        targets += add_target(instruction)
        zero_flag += add_zero(instruction)
        negative_flag += add_negative(instruction)
        carry_flag += add_carry(instruction)
        overflow_flag += add_overflow(instruction)

        classical_memory_needed += add_classical(instruction, register_size)

        for operand in instruction:
            if '#' not in operand:
                try:
                    highest_register = max(int(operand.replace('{','').replace('}','').replace('R', '')), highest_register)

                except ValueError:
                    pass

        print(instruction, classical_memory_needed)

    print(highest_register)

    return (highest_register+1)*register_size+targets+zero_flag+negative_flag+carry_flag+overflow_flag, ancilla, targets, zero_flag, negative_flag, carry_flag, overflow_flag, classical_memory_needed

def get_parameters(assembly_program):
    with open(assembly_program, 'r') as file:
        parameters = json.loads(file.readline())
        print(parameters)

    return parameters


def reverse_oracle(qc, oracle_qc):
    print("Reverse Oracle")
    print([i for i in range(qc.num_qubits)])
    reverse_oracle_qc = oracle_qc.inverse()
    print(qc.num_qubits)
    print(reverse_oracle_qc.num_qubits)
    reverse_oracle_qc.name = 'REV'

    # qc.barrier()
    # qc.barrier()
    # # decomposed_reverse_oracle = reverse_oracle_qc.decompose()
    # for instr, qargs, cargs in reverse_oracle_qc.data:
    #     print(instr, [qc.qubits[i.index+1] for i in qargs], cargs)
    #     qc.append(instr, [qc.qubits[i.index+1] for i in qargs], cargs)
    # qc.barrier()
    # qc.barrier()


    qc.append(reverse_oracle_qc, [i for i in range(qc.num_qubits)])




def evaluate_instruction(instruction, qc, cr, in_oracle, register_size, ancilla_counter, additional_flags, targets_counter, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags):
    operation = instruction[0]
    op1 = op2 = op3 = op4 = None
    if len(instruction) > 1:
        op1 = instruction[1]
    if len(instruction) > 2:
        op2 = instruction[2]
    if len(instruction) > 3:
        op3 = instruction[3]
    if len(instruction) > 4:
        op4 = instruction[4]

    print("in_oracle", in_oracle)

    if instruction[0] == 'ADC':
        carry_flag_counter += 1
        ancilla_counter = ADC(qc, register_size, ancilla_counter, additional_flags, carry_flag_counter, carry_flags, op1, op2, op3)
    elif instruction[0] == 'ADD':
        ancilla_counter = ADD(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3)
    elif instruction[0] == 'AND':
        ancilla_counter = AND(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3)
    elif instruction[0] == 'BIC':
        ancilla_counter = BIC(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3)
    elif instruction[0] == 'CMN':
        # increment flags before the operation. Akin to refreshing the flags
        zero_flag_counter += 1
        negative_flag_counter += 1
        carry_flag_counter += 1
        overflow_flag_counter += 1
        ancilla_counter = CMN(qc, register_size, ancilla_counter, additional_flags, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags, op1, op2)
    elif instruction[0] == 'CMP':
        # increment flags before the operation. Akin to refreshing the flags
        zero_flag_counter += 1
        negative_flag_counter += 1
        carry_flag_counter += 1
        overflow_flag_counter += 1
        print(carry_flag_counter, carry_flags)
        ancilla_counter = CMP(qc, register_size, ancilla_counter, additional_flags, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags, op1, op2)
    elif instruction[0] == 'EOR':
        ancilla_counter = EOR(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3)
    elif instruction[0] == 'LSL':
        LSL(qc, register_size, additional_flags, op1, op2, op3)
    elif instruction[0] == 'LSR':
        LSR(qc, register_size, additional_flags, op1, op2, op3)
    elif instruction[0] == 'MLA':
        ancilla_counter = MLA(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3, op4)
    elif instruction[0] == 'MOV':
        MOV(qc, register_size, additional_flags, op1, op2)
    elif instruction[0] == 'MRS':
        MRS(qc, register_size, additional_flags, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags, op1)
    elif instruction[0] == 'MSR':
        # increment flags before the operation. Akin to refreshing the flags
        zero_flag_counter += 1
        negative_flag_counter += 1
        carry_flag_counter += 1
        overflow_flag_counter += 1
        MSR(qc, register_size, additional_flags, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags, op1)
    elif instruction[0] == 'MUL':
        ancilla_counter = MUL(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3)
    elif instruction[0] == 'MVN':
        MVN(qc, register_size, additional_flags, op1, op2)
    elif instruction[0] == 'ORR':
        ancilla_counter = ORR(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3)
    elif instruction[0] == 'RSB':
        ancilla_counter = RSB(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3)
    elif instruction[0] == 'RSC':
        ancilla_counter = RSC(qc, register_size, ancilla_counter, additional_flags, carry_flag_counter, carry_flags, op1, op2, op3)
    elif instruction[0] == 'SBC':
        ancilla_counter = SBC(qc, register_size, ancilla_counter, additional_flags, carry_flag_counter, carry_flags, op1, op2, op3)
    elif instruction[0] == 'STR':
        if in_oracle:
            raise Exception('Cannot apply operation while in the oracle')

        STR(qc, cr, register_size, additional_flags, op1, op2, op3)
    elif instruction[0] == 'SUB':
        ancilla_counter = SUB(qc, register_size, ancilla_counter, additional_flags, op1, op2, op3)
    elif instruction[0] == 'TEQ':
        # increment flags before the operation. Akin to refreshing the flags
        zero_flag_counter += 1
        negative_flag_counter += 1
        carry_flag_counter += 1
        overflow_flag_counter += 1
        ancilla_counter = TEQ(qc, register_size, ancilla_counter, additional_flags, zero_flag_counter, negative_flag_counter, overflow_flag_counter, zero_flags, negative_flags, overflow_flags, op1, op2)
    elif instruction[0] == 'TST':
        # increment flags before the operation. Akin to refreshing the flags
        zero_flag_counter += 1
        negative_flag_counter += 1
        carry_flag_counter += 1
        overflow_flag_counter += 1
        ancilla_counter = TST(qc, register_size, ancilla_counter, additional_flags, zero_flag_counter, negative_flag_counter, overflow_flag_counter, zero_flags, negative_flags, overflow_flags, op1, op2)
    elif instruction[0] == 'HAD':
        HAD(qc, register_size, additional_flags, op1)
    elif instruction[0] == 'XXX':
        XXX(qc, register_size, additional_flags, op1)
    elif instruction[0] == 'TGT':
        if in_oracle:
            raise Exception('Cannot apply operation while in the oracle')

        targets_counter += 1
        TGT(qc, register_size, additional_flags, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags, op1)
    elif instruction[0] == 'MCT':
        if in_oracle:
            raise Exception('Cannot apply operation while in the oracle')

        targets_counter += 1
        MCT(qc, register_size, additional_flags, op1)
    elif instruction[0] == 'DIF':
        if in_oracle:
            raise Exception('Cannot apply operation while in the oracle')

        DIF(qc, register_size, additional_flags, instruction[1:])
    elif instruction[0] == 'BAR':
        BAR(qc)
    elif instruction[0] == 'ORACLE':
        in_oracle = True
    elif instruction[0] == 'END_ORACLE':
        in_oracle = False
    else:
        raise ValueError('Invalid Instruction')

    return in_oracle, ancilla_counter, targets_counter, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter



def decode(register_size, decoding, results):
    if decoding is None:
        print('Results:', results)
        return

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    for result in sorted_results:
        print('# Measurements:', result[1])
        for classical_register in decoding.keys():
            print(decoding[classical_register], end=': ')
            for i in reversed(get_classical_register_location(register_size, classical_register)):
                print(result[0][::-1][i], end='')

            print()



def assembly_to_qiskit(assembly_program):
    # debug_memory = [1, 5,6,7,8,9,10,14]
    debug_memory = [0,1,2,3]
    parameters = get_parameters(assembly_program)
    register_size = parameters.get('register_size', 2)
    decoding = parameters.get('decoding', None)
    run = parameters.get('run', True)
    display = parameters.get('display', True)
    instructions = get_instructions(assembly_program)
    name = assembly_program.split('.')[0]
    targets = None
    zero_flags = None
    negative_flags = None
    carry_flags = None
    overflow_flags = None

    ancilla_counter, num_ancilla, targets_count, zero_flags_count, negative_flags_count, carry_flags_count, overflow_flags_count, classical_memory_needed = initialize(instructions, register_size)
    print('ancilla_counter:', ancilla_counter)
    print('num_ancilla:', num_ancilla)

    print('zero_flags_count:', zero_flags_count)
    print('negative_flags_count:', negative_flags_count)
    print('carry_flags_count:', carry_flags_count)
    print('overflow_flags_count:', overflow_flags_count)


    targets_counter = -1
    zero_flag_counter = -1
    negative_flag_counter = -1
    carry_flag_counter = -1
    overflow_flag_counter = -1

    if targets_count > 0:
        targets = QuantumRegister(targets_count, 'targets')

    if zero_flags_count > 0:
        zero_flags = QuantumRegister(zero_flags_count, 'zero_flags')

    if negative_flags_count > 0:
        negative_flags = QuantumRegister(negative_flags_count, 'negative_flags')
    
    if carry_flags_count > 0:
        carry_flags = QuantumRegister(carry_flags_count, 'carry_flags')
    
    if overflow_flags_count > 0:
        overflow_flags = QuantumRegister(overflow_flags_count, 'overflow_flags')


    qr = QuantumRegister(ancilla_counter - zero_flags_count - negative_flags_count - carry_flags_count - overflow_flags_count - targets_count + num_ancilla, 'qr')

    if classical_memory_needed == 0:
        raise Exception('Must use at least one STR or STM operation')

    cr = ClassicalRegister(classical_memory_needed)
    # cr = ClassicalRegister(len(debug_memory))


    if carry_flags_count > 0:
        if targets_count > 0:
            if zero_flags_count > 0:
                qc = QuantumCircuit(targets, zero_flags, negative_flags, carry_flags, overflow_flags, qr, cr)
                oracle_qc = QuantumCircuit(targets, zero_flags, negative_flags, carry_flags, overflow_flags, qr)
            elif carry_flags_count > 0:
                qc = QuantumCircuit(targets, carry_flags, qr, cr)
                oracle_qc = QuantumCircuit(targets, carry_flags, qr)
            else:
                qc = QuantumCircuit(targets, qr, cr)
                oracle_qc = QuantumCircuit(targets, qr)
        else:
            if zero_flags_count > 0:
                qc = QuantumCircuit(zero_flags, negative_flags, carry_flags, overflow_flags, qr, cr)
                oracle_qc = QuantumCircuit(zero_flags, negative_flags, carry_flags, overflow_flags, qr)
            elif carry_flags_count > 0:
                qc = QuantumCircuit(carry_flags, qr, cr)
                oracle_qc = QuantumCircuit(carry_flags, qr)
            else:
                qc = QuantumCircuit(qr, cr)
                oracle_qc = QuantumCircuit(qr)
    else:
        if targets_count > 0:
            if zero_flags_count > 0:
                qc = QuantumCircuit(targets, zero_flags, negative_flags, overflow_flags, qr, cr)
                oracle_qc = QuantumCircuit(targets, zero_flags, negative_flags, overflow_flags, qr)
            elif carry_flags_count > 0:
                qc = QuantumCircuit(targets, carry_flags, qr, cr)
                oracle_qc = QuantumCircuit(targets, carry_flags, qr)
            else:
                qc = QuantumCircuit(targets, qr, cr)
                oracle_qc = QuantumCircuit(targets, qr)
        else:
            if zero_flags_count > 0:
                qc = QuantumCircuit(zero_flags, negative_flags, overflow_flags, qr, cr)
                oracle_qc = QuantumCircuit(zero_flags, negative_flags, overflow_flags, qr)
            elif carry_flags_count > 0:
                qc = QuantumCircuit(carry_flags, qr, cr)
                oracle_qc = QuantumCircuit(carry_flags, qr)
            else:
                qc = QuantumCircuit(qr, cr)
                oracle_qc = QuantumCircuit(qr)


    
    in_oracle = False

    additional_flags = targets_count + zero_flags_count + negative_flags_count + carry_flags_count + overflow_flags_count

    for i, instruction in enumerate(instructions):
        if i < 1:
            continue

        print()
        print('ancilla_counter:', ancilla_counter)
        print(instruction)

        if instruction[0] == 'REVERSE_ORACLE':
            # apply the reverse over the entire quantum circuit + 1 (ignore the target qubit)
            reverse_oracle(qc, oracle_qc)
        else:
            if in_oracle:
                in_oracle, disregard0, disregard1, disregard2, disregard3, disregard4, disregard5 = evaluate_instruction(instruction, oracle_qc, cr, in_oracle, register_size, ancilla_counter, additional_flags, targets_counter, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags)

            in_oracle, ancilla_counter, targets_counter, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter = evaluate_instruction(instruction, qc, cr, in_oracle, register_size, ancilla_counter, additional_flags, targets_counter, zero_flag_counter, negative_flag_counter, carry_flag_counter, overflow_flag_counter, zero_flags, negative_flags, carry_flags, overflow_flags)

    # for i in range(len(debug_memory)):
    #     qc.measure(debug_memory[i], i)

    return qc, name, run, display, register_size, decoding



def run_assembly(filename):
    qc, name, run, display, register_size, decoding = assembly_to_qiskit(filename)

    name = name.replace('assembly_programs/','').replace('operations/', '').replace('automatically_generated/', '')

    # decomposed_qc = qc.decompose()

    qc.draw(output='mpl', filename='Figures/'+name+'_circuit.png', fold=140)



    if run:
        qasm_simulator = Aer.get_backend('qasm_simulator')
        shots = 2000
        results = execute(qc, backend=qasm_simulator, shots=shots).result()
        answer = results.get_counts()
        
        print()
        decode(register_size, decoding, answer)
        print()

        # Redirect standard error
        original_stderr = sys.stderr
        sys.stderr = io.StringIO()

        hist = plot_histogram(answer)
        plt.subplots_adjust(bottom=0.4)
        plt.savefig('Figures/'+name+'_hist.png')

        # Restore standard error
        sys.stderr = original_stderr

    if display:
        # Redirect standard error
        original_stderr = sys.stderr
        sys.stderr = io.StringIO()

        print()
        plt.show()

        # Restore standard error
        sys.stderr = original_stderr


if __name__ == '__main__':
    run_assembly(sys.argv[1])






