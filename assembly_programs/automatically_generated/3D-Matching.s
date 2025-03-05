{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Load the values of R0 and R1 into R2 and R3
MOV R2, R0
MOV R3, R1

; XOR R2 and R3 to find the differences, store result in R4
EOR R4, R2, R3

; Check if the result is zero (i.e., R0 == R1)
TST R4, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

