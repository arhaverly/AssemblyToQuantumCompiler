{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Subtract 1 from R0 and store the result in R2
SUB R2, R0, #1
; Subtract 1 from R1 and store the result in R3
SUB R3, R1, #1

; Perform a bitwise AND operation on R2 and R3 to check if both are non-negative
AND R4, R2, R3

; Perform a bitwise OR operation on R2 and R3 to check if both are less than or equal to 1
ORR R5, R2, R3

; Perform a bitwise AND operation on the inverted R4 and R5 to check if both conditions are met
MVN R6, R4
AND R7, R6, R5

; Set the ZERO PSR flag based on R7
; If R7 is non-zero, then both R0 and R1 are <= 1 and it's a valid solution
TST R7, #1



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

