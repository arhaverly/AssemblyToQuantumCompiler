{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Compare R0 with 3
MOV R2, #3
CMP R0, R2

; If R0 = 3, set R3 to 1, else set R3 to 0
MOV R3, #1
MOV R4, #0
EOR R3, R4, R3, eq

; Compare R1 with 3
CMP R1, R2

; If R1 = 3, set R4 to 1, else set R4 to 0
MOV R4, #1
MOV R5, #0
EOR R4, R5, R4, eq

; If both R0 and R1 are 3, AND R3 and R4 will be 1, else it will be 0
AND R6, R3, R4

; Set the ZERO PSR flag to the result in R6
TST R6, #1



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

