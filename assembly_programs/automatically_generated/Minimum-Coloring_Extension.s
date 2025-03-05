{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Subtract R1 from R0, and store the result in R2
SUB R2, R0, R1

; Perform bitwise AND between R2 and 3 (0b11) to get the last 2 bits, store the result in R3
AND R3, R2, #3

; Use TEQ to compare R3 with 0 and set the ZERO PSR flag
TEQ R3, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

