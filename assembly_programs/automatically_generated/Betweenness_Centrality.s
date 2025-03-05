{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Let's assume R0 = a, R1 = b for the Betweenness Centrality problem.
; The valid solution is when a + b = 3, so we need to check if a + b - 3 = 0.

; Move the value of R0 to R2
MOV R2, R0

; Add the value of R1 to R2
ADD R3, R2, R1

; Subtract 3 from R3
SUB R4, R3, #3

; Check if R4 equals zero and store the result in the ZERO PSR flag
CMP R4, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

