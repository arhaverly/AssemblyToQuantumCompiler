{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Initialize R2 to store 3 (the maximum allowed number of vertices)
MOV R2, #3

; Add the values in R0 and R1, store the result in R3
ADD R3, R0, R1

; Compare R3 with R2, setting the ZERO flag if R3 <= R2
SUB R4, R2, R3
CMP R4, #0
MOV R5, R4 ; Move R4 to R5 to avoid using R4 twice in an instruction
TEQ R5, #0 ; Set ZERO flag if result is zero (R3 <= R2)



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

