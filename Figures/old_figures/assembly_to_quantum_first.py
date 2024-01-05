# Andrew Haverly
# Look at the paper for explanations
# Comments == lame


#initialization
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

# importing Qiskit
from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.providers.ibmq import least_busy
from qiskit.circuit.library import IntegerComparator
from qiskit.providers.aer import QasmSimulator


from qiskit.circuit.library import MCMT, CSwapGate, CHGate


import random

# import basic plot tools
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor



def qor():
    qc = QuantumCircuit(3)

    qc.x(0)
    qc.x(1)

    qc.ccx(0,1,2)
    qc.x(0)
    qc.x(1)
    qc.x(2)

    QOR = qc.to_gate()
    QOR.name = "M_QOR"
    return QOR


def full_adder(qc, A, B, Cin, Sum, Cout):
    qc.cx(A, Sum)
    qc.cx(B, Sum)

    if Cin != None:
        qc.cx(Cin, Sum)

    if Cout != None:
        qc.mct([A, B], Cout)

        if Cin != None:
            qc.mct([A, Cin], Cout)
            qc.mct([B, Cin], Cout)



def ripple_carry_adder2(qc, Rd, Rn, Operand, CarryRegister, CarryFlag):
    # qc.barrier()
    full_adder(qc, Rn[0], Operand[0], None, Rd[0], CarryRegister[0])
    qc.barrier()
    if CarryFlag != None:
        full_adder(qc, Rn[1], Operand[1], CarryRegister[0], Rd[1], CarryFlag[0])
    else:
        full_adder(qc, Rn[1], Operand[1], CarryRegister[0], Rd[1], None)
    qc.barrier()



def ripple_carry_adder3(qc, Rd, Rn, Operand, CarryRegister, CarryFlag):
    # qc.barrier()
    full_adder(qc, Rn[0], Operand[0], None, Rd[0], CarryRegister[0])
    qc.barrier()

    full_adder(qc, Rn[1], Operand[1], CarryRegister[0], Rd[1], CarryRegister[1])

    if CarryFlag != None:
        full_adder(qc, Rn[2], Operand[2], CarryRegister[1], Rd[2], CarryFlag[0])
    else:
        full_adder(qc, Rn[2], Operand[2], CarryRegister[1], Rd[2], None)
    qc.barrier()




def ADC():
    name = 'ADC'
    n = 2

    CarryFlag = QuantumRegister(1, 'carryFlag')
    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    CarryRegister = QuantumRegister(n-1, 'carryRegister')

    cr = ClassicalRegister(3)

    qc = QuantumCircuit(CarryFlag, Rn, Op2, CarryRegister, Rd, cr)

    # qc.x(Rn[0])
    # qc.x(Op2[0])

    ripple_carry_adder2(qc, Rd, Rn, Op2, CarryRegister, CarryFlag)

    qc.measure(Rd, cr[0:2])
    qc.measure(CarryFlag, cr[2])

    return qc, name



def ADD():
    name = 'ADD'
    n = 2

    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Operand = QuantumRegister(n, 'op2')
    CarryRegister = QuantumRegister(n-1, 'carryRegister')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rn, Op2, CarryRegister, Rd, cr)

    # qc.x(Rn[0])
    # qc.x(Op2[0])

    ripple_carry_adder2(qc, Rd, Rn, Op2, CarryRegister, None)

    qc.measure(Rd, cr)
    # qc.measure(CarryFlag, cr[2])

    return qc, name


def AND():
    name = 'AND'
    n = 2

    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rn, Op2, Rd, cr)

    # qc.x(Rn[0])
    # qc.x(Op2[0])


    qc.mct([Rn, Op2], Rd)

    qc.barrier()

    qc.measure(Rd, cr)
    # qc.measure(CarryFlag, cr[2])

    return qc, name



def BIC():
    name = 'BIC'
    n = 2

    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rn, Op2, Rd, cr)

    # qc.x(Rn[0])
    # qc.x(Op2[0])

    qc.x(Op2)
    qc.mct([Rn, Op2], Rd)

    qc.barrier()

    qc.measure(Rd, cr)
    # qc.measure(CarryFlag, cr[2])

    return qc, name



def CMN():
    name = 'CMN'
    n = 2

    ZeroFlag = QuantumRegister(1, 'zeroFlag')
    NegativeFlag = QuantumRegister(1, 'negativeFlag')
    CarryFlag = QuantumRegister(1, 'carryFlag')
    OverflowFlag = QuantumRegister(1, 'overflowFlag')

    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    CarryRegister = QuantumRegister(n-1, 'carryAncRegister')
    OverflowAncRegister = QuantumRegister(2, 'overflowAncRegister')


    cr = ClassicalRegister(4)

    qc = QuantumCircuit(ZeroFlag, NegativeFlag, CarryFlag, OverflowFlag, Rn, Op2, CarryRegister, OverflowAncRegister, Rd, cr)

    # qc.x(Rn[1])
    # qc.x(Op2[1])

    ripple_carry_adder2(qc, Rd, Rn, Op2, CarryRegister, CarryFlag)

    # zero
    qc.barrier()
    qc.x(Rd)
    qc.mct(Rd, ZeroFlag)
    qc.x(Rd)

    # negative
    qc.barrier()
    qc.cx(Rd[n-1], NegativeFlag)

    # overflow
    # occurs when the two operands have the same sign (both positive or both negative), but the result has a different sign
    qc.barrier()
    qc.x(Rn[1])
    qc.x(Op2[1])
    qc.mct([Rn[1], Op2[1], Rd[1]], OverflowAncRegister[0])
    qc.x(Rn[1])
    qc.x(Op2[1])

    qc.x(Rd[1])
    qc.mct([Rn[1], Op2[1], Rd[1]], OverflowAncRegister[1])
    qc.x(Rd[1])

    qc.append(qor(), [OverflowAncRegister[0], OverflowAncRegister[1], OverflowFlag])


    qc.barrier()

    qc.measure(ZeroFlag, cr[0])
    qc.measure(NegativeFlag, cr[1])
    qc.measure(CarryFlag, cr[2])
    qc.measure(OverflowFlag, cr[3])

    return qc, name



def CMP():
    name = 'CMP'
    n = 2

    ZeroFlag = QuantumRegister(1, 'zeroFlag')
    NegativeFlag = QuantumRegister(1, 'negativeFlag')
    CarryFlag = QuantumRegister(1, 'carryFlag')
    OverflowFlag = QuantumRegister(1, 'overflowFlag')

    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    CarryRegister = QuantumRegister(n-1, 'carryAncRegister')
    OverflowAncRegister = QuantumRegister(2, 'overflowAncRegister')
    AdditionAncRegister = QuantumRegister(n, 'addAncRegister')
    NegatedOp2 = QuantumRegister(n, 'addAncRegister2')

    cr = ClassicalRegister(4)

    qc = QuantumCircuit(ZeroFlag, NegativeFlag, CarryFlag, OverflowFlag, Rn, Op2, CarryRegister, OverflowAncRegister, AdditionAncRegister, NegatedOp2, Rd, cr)

    # qc.x(Rn[1])
    # qc.x(Op2[1])


    # take the twos complement of Op2 (invert and add 1)
    qc.barrier()
    qc.x(AdditionAncRegister[0])
    qc.x(Op2)
    ripple_carry_adder2(qc, NegatedOp2, AdditionAncRegister, Op2, CarryRegister, None)
    qc.reset(CarryRegister)
    qc.barrier()



    ripple_carry_adder2(qc, Rd, Rn, NegatedOp2, CarryRegister, CarryFlag)

    # zero
    qc.barrier()
    qc.x(Rd)
    qc.mct(Rd, ZeroFlag)
    qc.x(Rd)

    # negative
    qc.barrier()
    qc.cx(Rd[n-1], NegativeFlag)

    # overflow
    # occurs when the two operands have the same sign (both positive or both negative), but the result has a different sign
    qc.barrier()
    qc.x(Rn[1])
    qc.x(NegatedOp2[1])
    qc.mct([Rn[1], NegatedOp2[1], Rd[1]], OverflowAncRegister[0])
    qc.x(Rn[1])
    qc.x(NegatedOp2[1])

    qc.x(Rd[1])
    qc.mct([Rn[1], NegatedOp2[1], Rd[1]], OverflowAncRegister[1])
    qc.x(Rd[1])

    qc.append(qor(), [OverflowAncRegister[0], OverflowAncRegister[1], OverflowFlag])


    qc.barrier()

    qc.measure(ZeroFlag, cr[0])
    qc.measure(NegativeFlag, cr[1])
    qc.measure(CarryFlag, cr[2])
    qc.measure(OverflowFlag, cr[3])

    return qc, name



def EOR():
    name = 'EOR'
    n = 2

    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    RnAndNotOp2 = QuantumRegister(n, 'rnAndNotOp2')
    Op2AndNotRn = QuantumRegister(n, 'op2AndNotRn')


    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rn, Op2, RnAndNotOp2, Op2AndNotRn, Rd, cr)

    qc.x(Op2)
    qc.mct([Rn, Op2], RnAndNotOp2)
    qc.x(Op2)

    qc.barrier()

    qc.x(Rn)
    qc.mct([Rn, Op2], Op2AndNotRn)
    qc.x(Rn)

    qc.barrier()

    qc.append(qor(), [RnAndNotOp2, Op2AndNotRn, Rd])

    qc.barrier()

    qc.measure(Rd, cr)

    return qc, name



def LDM():
    name = 'LDM'
    n = 2

    Rn1 = QuantumRegister(n, 'rn1')
    Rn2 = QuantumRegister(n, 'rn2')
    cr = ClassicalRegister(2*n)

    qc = QuantumCircuit(Rn1, Rn2, cr)

    qc.initialize([1, 0], Rn1[0])
    qc.initialize([0, 1], Rn1[1])

    qc.initialize([1, 0], Rn2[0])
    qc.initialize([0, 1], Rn2[1])

    qc.barrier()

    qc.measure(Rn1, cr[0:2])
    qc.measure(Rn2, cr[2:4])

    return qc, name


def LDR():
    name = 'LDR'
    n = 2

    Rn = QuantumRegister(n, 'rn')
    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rn, cr)

    qc.initialize([1, 0], Rn[0])
    qc.initialize([0, 1], Rn[1])

    qc.barrier()

    qc.measure(Rn, cr)

    return qc, name



# the immediate value is classically determined and put into the swap gates
# if needed to conditionally control the amount of shifting, turn into a one-hot encoded and shift off of that single control
def LSL():
    name = 'LSL'
    n = 2

    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    ancilla = QuantumRegister(1, 'ancilla')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rn, ancilla, Rd, cr)

    qc.cx(Rn, Rd)
    qc.swap(Rd[n-1], ancilla)
    qc.swap(Rd[0], Rd[1])
    
    qc.barrier()

    qc.measure(Rd, cr)

    return qc, name



# the immediate value is classically determined and put into the swap gates
# if needed to conditionally control the amount of shifting, turn into a one-hot encoded and shift off of that single control
def LSR():
    name = 'LSR'
    n = 2

    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    ancilla = QuantumRegister(1, 'ancilla')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rn, ancilla, Rd, cr)

    qc.cx(Rn, Rd)
    qc.swap(Rd[0], ancilla)
    qc.swap(Rd[0], Rd[1])
    
    qc.barrier()

    qc.measure(Rd, cr)

    return qc, name


def MLA():
    name = 'MLA'
    n = 2

    Rd = QuantumRegister(2*n, 'rd')
    Rm = QuantumRegister(n, 'rm')
    Rs = QuantumRegister(n, 'rs')
    Rn = QuantumRegister(n, 'rn')

    Ancilla = QuantumRegister(7, 'ancilla')
    MUL_Result = QuantumRegister(2*n, 'mul_result')

    cr = ClassicalRegister(4)

    qc = QuantumCircuit(Rm, Rs, Rn, Ancilla, MUL_Result, Rd, cr)

    # qc.x(Rm)
    # qc.x(Rs[1])
    # qc.x(Rn)

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


    qc.barrier()

    qc.measure(Rd, cr)

    return qc, name


def MOV():
    name = 'MOV'
    n = 2

    Rd = QuantumRegister(n, 'rd')
    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rd, cr)

    qc.initialize([1, 0], Rd[0])
    qc.initialize([0, 1], Rd[1])

    qc.barrier()

    qc.measure(Rd, cr)

    return qc, name


def MRS():
    name = 'MRS'
    n = 4

    PSR = QuantumRegister(n, 'psr')
    Rn = QuantumRegister(n, 'rn')
    cr = ClassicalRegister(4)

    qc = QuantumCircuit(PSR, Rn, cr)

    qc.cx(PSR, Rn)

    qc.barrier()

    qc.measure(Rn, cr)

    return qc, name



def MSR():
    name = 'MSR'
    n = 4

    PSR = QuantumRegister(n, 'psr')
    Rn = QuantumRegister(n, 'rn')
    cr = ClassicalRegister(4)

    qc = QuantumCircuit(PSR, Rn, cr)

    qc.cx(Rn, PSR)

    qc.barrier()

    qc.measure(PSR, cr)

    return qc, name



def MUL():
    name = 'MUL'
    n = 2

    Rd = QuantumRegister(2*n, 'rd')
    Rm = QuantumRegister(n, 'rm')
    Rs = QuantumRegister(n, 'rs')

    Ancilla = QuantumRegister(4, 'ancilla')

    cr = ClassicalRegister(4)

    qc = QuantumCircuit(Rm, Rs, Ancilla, Rd, cr)

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

    
    qc.barrier()

    qc.measure(Rd, cr)

    return qc, name


def MVN():
    name = 'MVN'
    n = 2

    Op2 = QuantumRegister(n, 'op2')
    Rd = QuantumRegister(n, 'rd')
    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Op2, Rd, cr)

    qc.cx(Op2, Rd)
    qc.x(Rd)

    qc.barrier()

    qc.measure(Rd, cr)

    return qc, name


def ORR():
    name = 'ORR'
    n = 2

    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    Rd = QuantumRegister(n, 'rd')
    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rn, Op2, Rd, cr)

    qc.x(Rn[0])
    qc.x(Op2[0])

    qc.ccx(Rn[0], Op2[0], Rd[0])
    qc.x(Rn[0])
    qc.x(Op2[0])
    qc.x(Rd[0])

    qc.barrier()

    qc.x(Rn[1])
    qc.x(Op2[1])

    qc.ccx(Rn[1], Op2[1], Rd[1])
    qc.x(Rn[1])
    qc.x(Op2[1])
    qc.x(Rd[1])

    qc.barrier()

    qc.measure(Rd, cr)

    return qc, name

# Rd := Op2 - Rn
def RSB():
    name = 'RSB'
    n = 2

    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    CarryRegister = QuantumRegister(n-1, 'carryAncRegister')
    AdditionAncRegister = QuantumRegister(n, 'addAncRegister')
    NegatedRn = QuantumRegister(n, 'addAncRegister2')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rn, Op2, CarryRegister, AdditionAncRegister, NegatedRn, Rd, cr)

    qc.x(Rn[0])
    qc.x(Op2[1])
    qc.barrier()

    # take the twos complement of Rn (invert and add 1)
    qc.x(AdditionAncRegister[0])
    qc.x(Rn)
    ripple_carry_adder2(qc, NegatedRn, AdditionAncRegister, Rn, CarryRegister, None)
    qc.reset(CarryRegister)
    qc.barrier()

    # add the two
    ripple_carry_adder2(qc, Rd, Rn, NegatedRn, CarryRegister, None)

    qc.measure(Rd, cr)

    return qc, name

# Rd := Op2 - Rn - 1 + Carry
def RSC():
    name = 'RSC'
    n = 2

    CarryFlag = QuantumRegister(n, 'carryFlag')
    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    Negative1 = QuantumRegister(n, 'negative1')
    CarryRegister = QuantumRegister(n-1, 'carryAncRegister')
    AdditionAncRegister = QuantumRegister(n, 'addAncRegister')
    Op2MinusRn = QuantumRegister(n, 'op2MinusRn')
    Op2MinusRnMinus1 = QuantumRegister(n, 'op2MinusRnMinus1')
    NegatedRn = QuantumRegister(n, 'addAncRegister2')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(CarryFlag, Rn, Op2, CarryRegister, AdditionAncRegister, NegatedRn, Op2MinusRn, Negative1, Op2MinusRnMinus1, Rd, cr)

    # qc.x(Rn[1])
    # qc.x(Op2[0])
    # qc.barrier()

    # take the twos complement of Op2 (invert and add 1)
    qc.x(AdditionAncRegister[0])
    qc.x(Rn)
    ripple_carry_adder2(qc, NegatedRn, AdditionAncRegister, Rn, CarryRegister, None)
    qc.reset(CarryRegister)
    qc.barrier()

    # add the Op2 and NegatedRn
    ripple_carry_adder2(qc, Op2MinusRn, Op2, NegatedRn, CarryRegister, None)
    qc.reset(CarryRegister)


    # add -1
    qc.x(Negative1)

    ripple_carry_adder2(qc, Op2MinusRnMinus1, Op2MinusRn, Negative1, CarryRegister, None)
    qc.reset(CarryRegister)


    # add CarryFlag
    ripple_carry_adder2(qc, Rd, Op2MinusRnMinus1, CarryFlag, CarryRegister, None)
    qc.reset(CarryRegister)

    qc.measure(Rd, cr)

    return qc, name



# Rd := Rn - Op2 - 1 + Carry
def SBC():
    name = 'SBC'
    n = 2

    CarryFlag = QuantumRegister(n, 'carryFlag')
    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    Negative1 = QuantumRegister(n, 'negative1')
    CarryRegister = QuantumRegister(n-1, 'carryAncRegister')
    AdditionAncRegister = QuantumRegister(n, 'addAncRegister')
    RnMinusOp2 = QuantumRegister(n, 'rnMinusOp2')
    RnMinusOp2Minus1 = QuantumRegister(n, 'rnMinusOp2Minus1')
    NegatedOp2 = QuantumRegister(n, 'addAncRegister2')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(CarryFlag, Rn, Op2, CarryRegister, AdditionAncRegister, NegatedOp2, RnMinusOp2, Negative1, RnMinusOp2Minus1, Rd, cr)

    # qc.x(Rn[1])
    # qc.x(Op2[0])
    # qc.barrier()

    # take the twos complement of Op2 (invert and add 1)
    qc.x(AdditionAncRegister[0])
    qc.x(Op2)
    ripple_carry_adder2(qc, NegatedOp2, AdditionAncRegister, Op2, CarryRegister, None)
    qc.reset(CarryRegister)
    qc.barrier()

    # add the Rn and NegatedOp2
    ripple_carry_adder2(qc, RnMinusOp2, Rn, NegatedOp2, CarryRegister, None)
    qc.reset(CarryRegister)


    # add -1
    qc.x(Negative1)

    ripple_carry_adder2(qc, RnMinusOp2Minus1, RnMinusOp2, Negative1, CarryRegister, None)
    qc.reset(CarryRegister)


    # add CarryFlag
    ripple_carry_adder2(qc, Rd, RnMinusOp2Minus1, CarryFlag, CarryRegister, None)
    qc.reset(CarryRegister)

    qc.measure(Rd, cr)

    return qc, name





def STM():
    name = 'STM'
    n = 2

    Rn = QuantumRegister(n, 'rn')
    Rm = QuantumRegister(n, 'rm')
    cr = ClassicalRegister(2*n)

    qc = QuantumCircuit(Rn, Rm, cr)

    qc.measure(Rn, cr[0:n])
    qc.measure(Rm, cr[n:2*n])

    return qc, name


def STR():
    name = 'STR'
    n = 2

    Rd = QuantumRegister(n, 'rd')
    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rd, cr)

    qc.measure(Rd, cr)

    return qc, name



# Rd := Rn - Op2
def SUB():
    name = 'SUB'
    n = 2

    Rd = QuantumRegister(n, 'rd')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    CarryRegister = QuantumRegister(n-1, 'carryAncRegister')
    AdditionAncRegister = QuantumRegister(n, 'addAncRegister')
    NegatedOp2 = QuantumRegister(n, 'addAncRegister2')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rn, Op2, CarryRegister, AdditionAncRegister, NegatedOp2, Rd, cr)

    # qc.x(Rn[1])
    # qc.x(Op2[0])
    # qc.barrier()

    # take the twos complement of Op2 (invert and add 1)

    qc.x(AdditionAncRegister[0])
    qc.x(Op2)
    ripple_carry_adder2(qc, NegatedOp2, AdditionAncRegister, Op2, CarryRegister, None)
    qc.reset(CarryRegister)
    qc.barrier()

    # add the two
    ripple_carry_adder2(qc, Rd, Rn, NegatedOp2, CarryRegister, None)

    qc.measure(Rd, cr)

    return qc, name



# Rd := [Rn], [Rn] := Rm
def SWP():
    name = 'SWP'
    n = 2

    Rm = QuantumRegister(n, 'rm')
    Rd = QuantumRegister(n, 'rd')
    cr = ClassicalRegister(2)

    qc = QuantumCircuit(Rm, Rd, cr)

    qc.initialize([1, 0], Rd[0])
    qc.initialize([0, 1], Rd[1])
    qc.measure(Rm, cr)

    return qc, name


# CPSR flags := Rn EOR Op2
def TEQ():
    name = 'TEQ'
    n = 2

    ZeroFlag = QuantumRegister(1, 'zeroFlag')
    NegativeFlag = QuantumRegister(1, 'negativeFlag')
    CarryFlag = QuantumRegister(1, 'carryFlag')
    OverflowFlag = QuantumRegister(1, 'overflowFlag')

    Ancilla = QuantumRegister(n, 'ancilla')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    RnAndNotOp2 = QuantumRegister(n, 'rnAndNotOp2')
    Op2AndNotRn = QuantumRegister(n, 'op2AndNotRn')
    CarryRegister = QuantumRegister(n-1, 'carryAncRegister')
    OverflowAncRegister = QuantumRegister(2, 'overflowAncRegister')


    cr = ClassicalRegister(4)

    qc = QuantumCircuit(ZeroFlag, NegativeFlag, CarryFlag, OverflowFlag, Rn, Op2, CarryRegister, OverflowAncRegister, Ancilla, RnAndNotOp2, Op2AndNotRn, cr)

    # qc.x(Rn[1])
    # qc.x(Op2[1])

    # EOR
    qc.x(Op2)
    qc.mct([Rn, Op2], RnAndNotOp2)
    qc.x(Op2)

    qc.barrier()

    qc.x(Rn)
    qc.mct([Rn, Op2], Op2AndNotRn)
    qc.x(Rn)

    qc.barrier()

    qc.append(qor(), [RnAndNotOp2, Op2AndNotRn, Ancilla])

    qc.barrier()

    # zero
    qc.barrier()
    qc.x(Ancilla)
    qc.mct(Ancilla, ZeroFlag)
    qc.x(Ancilla)

    # negative
    qc.barrier()
    qc.cx(Ancilla[n-1], NegativeFlag)

    # overflow
    # occurs when the two operands have the same sign (both positive or both negative), but the result has a different sign
    qc.barrier()
    qc.x(Rn[1])
    qc.x(Op2[1])
    qc.mct([Rn[1], Op2[1], Ancilla[1]], OverflowAncRegister[0])
    qc.x(Rn[1])
    qc.x(Op2[1])

    qc.x(Ancilla[1])
    qc.mct([Rn[1], Op2[1], Ancilla[1]], OverflowAncRegister[1])
    qc.x(Ancilla[1])

    qc.append(qor(), [OverflowAncRegister[0], OverflowAncRegister[1], OverflowFlag])


    qc.barrier()

    qc.measure(ZeroFlag, cr[0])
    qc.measure(NegativeFlag, cr[1])
    qc.measure(CarryFlag, cr[2])
    qc.measure(OverflowFlag, cr[3])

    return qc, name




# CPSR flags := Rn AND Op2
def TST():
    name = 'TST'
    n = 2

    ZeroFlag = QuantumRegister(1, 'zeroFlag')
    NegativeFlag = QuantumRegister(1, 'negativeFlag')
    CarryFlag = QuantumRegister(1, 'carryFlag')
    OverflowFlag = QuantumRegister(1, 'overflowFlag')

    Ancilla = QuantumRegister(n, 'ancilla')
    Rn = QuantumRegister(n, 'rn')
    Op2 = QuantumRegister(n, 'op2')
    CarryRegister = QuantumRegister(n-1, 'carryAncRegister')
    OverflowAncRegister = QuantumRegister(2, 'overflowAncRegister')


    cr = ClassicalRegister(4)

    qc = QuantumCircuit(ZeroFlag, NegativeFlag, CarryFlag, OverflowFlag, Rn, Op2, CarryRegister, OverflowAncRegister, Ancilla, cr)

    # qc.x(Rn[1])
    # qc.x(Op2[1])


    # AND
    qc.mct([Rn, Op2], Ancilla)


    # zero
    qc.barrier()
    qc.x(Ancilla)
    qc.mct(Ancilla, ZeroFlag)
    qc.x(Ancilla)

    # negative
    qc.barrier()
    qc.cx(Ancilla[n-1], NegativeFlag)

    # overflow
    # occurs when the two operands have the same sign (both positive or both negative), but the result has a different sign
    qc.barrier()
    qc.x(Rn[1])
    qc.x(Op2[1])
    qc.mct([Rn[1], Op2[1], Ancilla[1]], OverflowAncRegister[0])
    qc.x(Rn[1])
    qc.x(Op2[1])

    qc.x(Ancilla[1])
    qc.mct([Rn[1], Op2[1], Ancilla[1]], OverflowAncRegister[1])
    qc.x(Ancilla[1])

    qc.append(qor(), [OverflowAncRegister[0], OverflowAncRegister[1], OverflowFlag])


    qc.barrier()

    qc.measure(ZeroFlag, cr[0])
    qc.measure(NegativeFlag, cr[1])
    qc.measure(CarryFlag, cr[2])
    qc.measure(OverflowFlag, cr[3])

    return qc, name


def fibonacci():
    name = 'fibonacci'
    n = 2

    R1 = QuantumRegister(n, 'r1')
    R2 = QuantumRegister(n, 'r2')
    R3 = QuantumRegister(n, 'r3')
    CarryRegister = QuantumRegister(n-1, 'carryRegister')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(R1, R2, R3, CarryRegister, cr)

    # MOV R1, #0
    qc.initialize([1,0], R1[0])
    qc.initialize([1,0], R1[1])

    # MOV R2, #1
    qc.initialize([0,1], R2[0])
    qc.initialize([1,0], R2[1])


    # Calculate F(2)
    # ADD R3, R1, R2
    ripple_carry_adder2(qc, R3, R1, R2, CarryRegister, None)
    qc.reset(CarryRegister)

    # MOV R1, R2
    qc.reset(R1)
    qc.cx(R2, R1)

    # MOV R2, R3
    qc.reset(R2)
    qc.cx(R3, R2)
    qc.reset(R3)

    qc.barrier()

    # Calculate F(3)
    # ADD R3, R1, R2
    ripple_carry_adder2(qc, R3, R1, R2, CarryRegister, None)
    qc.reset(CarryRegister)

    # MOV R1, R2
    qc.reset(R1)
    qc.cx(R2, R1)

    # MOV R2, R3
    qc.reset(R2)
    qc.cx(R3, R2)
    qc.reset(R3)

    qc.barrier()

    # Calculate F(4)
    # ADD R3, R1, R2
    ripple_carry_adder2(qc, R3, R1, R2, CarryRegister, None)
    qc.reset(CarryRegister)

    # MOV R1, R2
    qc.reset(R1)
    qc.cx(R2, R1)

    # MOV R2, R3
    qc.reset(R2)
    qc.cx(R3, R2)
    qc.reset(R3)

    

    qc.measure(R2, cr)

    return qc, name






'''
MOV R1, #0       ; Initialize R1 with 0, F(0)
MOV R2, #1       ; Initialize R2 with 1, F(1)

; calculate F(2)
ADD R3, R1, R2   ; R3 = R1 + R2, calculate the next Fibonacci number (F(2))

; calculate F(3)
ADD R4, R2, R3   ; R4 = R2 + R3, calculate the next Fibonacci number (F(3))

; calculate F(4)
ADD R5, R3, R4   ; R5 = R3 + R4, calculate the next Fibonacci number (F(4))
'''
def fibonacci_coherence_maintaining():
    name = 'fibonacci'
    n = 2

    R1 = QuantumRegister(n, 'r1')
    R2 = QuantumRegister(n, 'r2')
    R3 = QuantumRegister(n, 'r3')
    R4 = QuantumRegister(n, 'r4')
    R5 = QuantumRegister(n, 'r5')
    CarryRegister0 = QuantumRegister(n-1, 'carryRegister0')
    CarryRegister1 = QuantumRegister(n-1, 'carryRegister1')
    CarryRegister2 = QuantumRegister(n-1, 'carryRegister2')

    cr = ClassicalRegister(2)

    qc = QuantumCircuit(R1, R2, R3, R4, R5, CarryRegister0, CarryRegister1, CarryRegister2, cr)

    # MOV R1, #0       ; Initialize R1 with 0, F(0)
    qc.initialize([1,0], R1[0])
    qc.initialize([1,0], R1[1])

    # MOV R2, #1       ; Initialize R2 with 1, F(1)

    qc.initialize([0,1], R2[0])
    qc.initialize([1,0], R2[1])


    # ; calculate F(2)
    # ADD R3, R1, R2   ; R3 = R1 + R2, calculate the next Fibonacci number (F(2))
    ripple_carry_adder2(qc, R3, R1, R2, CarryRegister0, None)

    qc.barrier()

    # ; calculate F(3)
    # ADD R4, R2, R3   ; R4 = R2 + R3, calculate the next Fibonacci number (F(3))
    ripple_carry_adder2(qc, R4, R2, R3, CarryRegister1, None)

    qc.barrier()

    # ; calculate F(4)
    # ADD R5, R3, R4   ; R5 = R3 + R4, calculate the next Fibonacci number (F(4))
    ripple_carry_adder2(qc, R5, R3, R4, CarryRegister2, None)

    qc.measure(R5, cr)

    return qc, name








if __name__ == '__main__':
    # qc, name = ADC()
    # qc, name = ADD()
    # qc, name = AND()
    # qc, name = BIC()
    # qc, name = CMN()
    # qc, name = CMP()
    # qc, name = EOR()
    # qc, name = LDM()
    # qc, name = LDR()
    # qc, name = LSL()
    # qc, name = LSR()
    # qc, name = MLA()
    # qc, name = MUL()
    # qc, name = MOV()
    # qc, name = MRS()
    # qc, name = MSR()
    # qc, name = MVN()
    # qc, name = ORR()
    # qc, name = RSB()
    # qc, name = RSC()
    # qc, name = SBC()
    # qc, name = STM()
    # qc, name = STR()
    # qc, name = SUB()
    # qc, name = SWP()
    # qc, name = TEQ()
    # qc, name = TST()


    # qc, name = fibonacci()



    qasm_simulator = Aer.get_backend('qasm_simulator')
    shots = 10
    results = execute(qc, backend=qasm_simulator, shots=shots).result()
    answer = results.get_counts()

    qc.draw(output='mpl', filename='Figures/'+name+'_circuit.png', fold=140)

    print(answer)

    hist = plot_histogram(answer)
    plt.subplots_adjust(bottom=0.4)

    plt.savefig('Figures/'+name+'_hist.png')

    plt.show()

