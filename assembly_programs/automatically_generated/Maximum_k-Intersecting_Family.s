{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


    ; Calculate k * (k + 1)
    ADD R2, R1, #1      ; R2 = R1 + 1
    MOV R3, R1, LSL #1  ; R3 = R1 * 2 (shift left by 1)
    ADD R4, R1, R3      ; R4 = R1 + R3 (sum of k * (k + 1))
    
    ; Add the number of sets to the result
    ADD R5, R0, R4      ; R5 = R0 + R4 (number of sets + sum of k * (k + 1))
    
    ; Check if the result is less than or equal to 3
    SUB R6, R5, #3      ; R6 = R5 - 3
    MOV R7, R6          ; R7 = R6 (copy R6 to R7)
    TST R7, R6          ; Test R7 with R6 (if R6 <= 0, sets ZERO flag)



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

