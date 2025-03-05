{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

; Store the immediate value 6 in R2
MOV R2, #6

; Add R0 and R1, store the result in R3
ADD R3, R0, R1

; Subtract R2 from R3, store the result in R4
SUB R4, R3, R2

; Compare R4 with 0, setting the ZERO flag
CMP R4, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

