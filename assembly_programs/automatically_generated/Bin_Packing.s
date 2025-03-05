{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

    ; Subtract 3 from R0, store the result in R2
    SUB R2, R0, #3
    ; Subtract R1 from R2 (R2 = R2 - R1), store the result in R3
    SUB R3, R2, R1
    ; Perform a bitwise AND operation between R2 and R3, store the result in R4
    AND R4, R2, R3
    ; Find the 2's complement of R4, store the result in R5
    RSB R5, R4, #0
    ; Perform a bitwise AND operation between R4 and R5, store the result in R6
    AND R6, R4, R5
    ; Set the ZERO PSR flag by comparing R6 to 0
    CMP R6, #0


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

