{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

; R2 will store the result of bitwise AND operation between R0 and R1
AND R2, R0, R1

; R3 will store the result of bitwise OR operation between R2 and R1
ORR R3, R2, R1

; Set ZERO PSR flag to 1 if R3 is equal to R0, otherwise set it to 0
TST R3, R0


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

