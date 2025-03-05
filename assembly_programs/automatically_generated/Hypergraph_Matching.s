{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Compute the union of R0 and R1
ORR R2, R0, R1

; Compute the intersection of R0 and R1
AND R3, R0, R1

; Check if the union is equal to 15 (0b1111)
SUB R4, R2, #15

; Check if the intersection is equal to 0 (0b0000)
CMP R3, #0

; Set the ZERO PSR flag to 1 if both conditions are met, otherwise set it to 0
TEQ R4, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

