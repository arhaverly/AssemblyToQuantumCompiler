{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if R0 = 0 and R1 = 1
MOV R2, #0
MOV R3, #1
TEQ R0, R2
TEQ R1, R3
AND R4, R0, R1

; Check if R0 = 1 and R1 = 2
MOV R5, #1
MOV R6, #2
TEQ R0, R5
TEQ R1, R6
AND R7, R1, R0

; Check if R0 = 2 and R1 = 0
MOV R8, #2
TEQ R0, R8
TEQ R1, R2
AND R9, R0, R1

; Combine the results and set ZERO flag
ORR R10, R4, R7
ORR R11, R10, R9
CMP R11, #0
; ZERO flag will be set to 1 if R11 = 0, indicating a valid solution, otherwise 0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

