{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Store the difference between the values in R0 and R1 in R2
SUB R2, R0, R1

; Store the 2's complement (negation) of the difference in R3
RSB R3, R2, #0

; Perform bitwise OR on R2 and R3, store the result in R4
ORR R4, R2, R3

; Shift R4 right by 1 bit using LSR, which effectively divides it by 2
LSR R4, R4, #1

; Perform bitwise AND on R4 with 0x1, store the result in R5
AND R5, R4, #1

; Set the ZERO PSR flag based on the result in R5
CMP R5, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

