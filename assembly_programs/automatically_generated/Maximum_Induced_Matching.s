{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Subtract 1 from R1 and store the result in R2
SUB R2, R1, #1

; Perform bitwise AND between R2 and R1, store the result in R3
AND R3, R2, R1

; Perform bitwise OR between R3 and R1, store the result in R4
ORR R4, R3, R1

; Check if R4 is equal to R1
TEQ R4, R1

; Set R5 to 0 if R4 is equal to R1 (R1 <= 1), else set R5 to 1
EOR R5, R1, R4

; Store the result in the ZERO PSR flag
TST R5, #1



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

