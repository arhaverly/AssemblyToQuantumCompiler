{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if R0 (number of vertices) is greater than 0 and less than or equal to 3
; And check if R1 (number of colors) is greater than 0

; R0 and R1 are given values and cannot be changed
; Using R2 and R3 as temporary registers

; R2 = 1
MOV R2, #1

; R3 = 3
MOV R3, #3

; Check if R0 > 0 (R0 - 1)
SUB R2, R0, R2

; Check if R0 <= 3 (R0 - 3)
SUB R3, R0, R3

; Check if R1 > 0
SUB R4, R1, R2

; R5 = R2 AND R3, check if R0 > 0 AND R0 <= 3
AND R5, R2, R3

; R6 = R5 AND R4, check if (R0 > 0 AND R0 <= 3) AND R1 > 0
AND R6, R5, R4

; Check the final result and set the ZERO PSR flag accordingly
TST R6, R2



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

