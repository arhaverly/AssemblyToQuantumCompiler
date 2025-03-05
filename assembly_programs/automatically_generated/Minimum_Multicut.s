{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Load the values of R0 and R1 into R2 and R3 respectively
MOV R2, R0
MOV R3, R1

; Perform bitwise AND operation between R2 and R3, store the result in R4
AND R4, R2, R3

; Compare the result in R4 with 0
CMP R4, #0

; Set the ZERO flag based on the comparison (1 if R4 is 0, 0 otherwise)
; Note: CMN (Compare Negative) instruction can be used to set the ZERO flag
; based on the comparison, since it is equivalent to CMP with the negation of the second operand
CMN R4, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

