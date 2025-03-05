{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Subtract 3 from R1 to check if it's less than or equal to 3
SUB R2, R1, #3

; Perform a bitwise AND operation on R2 with its complement, if R2 <= 3, the result will be 0
MVN R3, R2
AND R4, R2, R3

; Compare R4 with 0
CMP R4, #0

; The ZERO PSR flag will be automatically set to 1 if R4 is 0 (equal), meaning R1 <= 3
; The ZERO PSR flag will be automatically set to 0 if R4 is not 0 (not equal), meaning R1 > 3



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

