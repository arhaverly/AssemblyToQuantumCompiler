{"register_size": 1, "run": true, "display": true}
HAD R0
HAD R1
HAD R2

ORACLE


; Calculate (a * b) by using AND operation
AND R3, R0, R1       ; R3 = a & b

; Calculate (b * c) by using AND operation
AND R4, R1, R2       ; R4 = b & c

; Calculate (a * b) + (b * c) by using ORR operation
ORR R5, R3, R4       ; R5 = (a & b) | (b & c)



END_ORACLE

TGT R5

REVERSE_ORACLE

DIF {R0, R1, R2}

STR CR0, R0
STR CR1, R1
STR CR2, R2

