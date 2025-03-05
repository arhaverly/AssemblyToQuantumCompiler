{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Move R0 into R2 and R1 into R3 since the original registers cannot be modified
MOV R2, R0
MOV R3, R1

; Compare if support count is greater than or equal to the minimum support threshold
; Subtract R3 (min support) from R2 (support count) and store the result in R4
SUB R4, R2, R3

; If R4 is positive or zero, then R0 >= R1 and it's a valid solution
; Perform bitwise AND with R4 and its complement, storing the result in R5
MVN R6, R4
AND R5, R4, R6

; Check if R5 is zero, indicating that R0 >= R1
; Set the ZERO flag accordingly
CMP R5, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

