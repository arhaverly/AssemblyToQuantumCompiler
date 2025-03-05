{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Load immediate values 3 and 0 into R2 and R3
MOV R2, #3
MOV R3, #0

; Subtract R0 from R2
SUB R4, R2, R0

; Add R1 to R4
ADD R5, R4, R1

; Invert R5
MVN R6, R5

; Add 4 to R6
ADD R7, R6, #4

; Perform AND operation on R7 and R2
AND R8, R7, R2

; Perform TST operation to update ZERO flag
TST R8, R2
; The ZERO flag is updated based on the result of the TST instruction
; If R8 = R2, then the ZERO flag will be 1 (valid solution)
; If R8 = R3, then the ZERO flag will be 0 (invalid solution)



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

