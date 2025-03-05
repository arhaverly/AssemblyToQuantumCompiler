{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Store the maximum allowed value (3) in R2
MOV R2, #3

; Compare R0 with R2 and store the result in R3
SUB R3, R2, R0

; Compare R1 with R2 and store the result in R4
SUB R4, R2, R1

; If both R3 and R4 are greater than or equal to 0, then R0 and R1 are within the allowed range
; Perform bitwise AND between R3 and R4, store the result in R5
AND R5, R3, R4

; Perform bitwise AND between R5 and the least significant bit of R5, store the result in R6
AND R6, R5, #1

; Compare R0 and R1 and store the result in R7
SUB R7, R0, R1

; Set the ZERO flag if R0 and R1 are equal and both are within the allowed range
; Calculate R7 AND R6, store the result in R8
AND R8, R7, R6

; Test if R8 is zero, set ZERO flag accordingly
TST R8, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

