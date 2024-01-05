{"register_size": 2}

; Explanation
; At the time of writing this, the subset sum problem is unsolved using
; Grover's Algorithm. As part of my thesis, the goal is to get an LLM
; to automatically write a program to solve an NP-Hard problem using
; Grover's Algorithm
;
; This is that solution. This was mostly written by GPT-4, with some
; Assembly-QuantumAssembly tweaks


; Subset Sum: With 2 bits, you can demonstrate a trivial case where the set contains two elements (each represented by one bit), and you are checking if their sum equals a target value (which must also be very small).






; put R0 and R1 into superposition
HAD R0
HAD R1


ORACLE
    ; load the target value
    MOV R2, #3 ; Load target sum into R1

    
    ; Calculate sum of two numbers
    ADD R3, R0, R1 ; Add the two numbers, result in R2

    CMP R3, R2 ; Compare sum with target
END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1






