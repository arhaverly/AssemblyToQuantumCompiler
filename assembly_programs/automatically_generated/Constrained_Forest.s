{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Load values into R2 and R3 for comparison
MOV R2, R0
MOV R3, R1

; Compare the values in R2 and R3
CMP R2, R3

; Set ZERO PSR flag based on the comparison
TST R2, R0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

