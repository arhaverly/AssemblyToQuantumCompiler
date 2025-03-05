{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if R0 (number of vertices) is even or odd
; by ANDing it with 1, storing the result in R2
AND R2, R0, #1

; If R0 is even, R2 = 0, else R2 = 1
; Add R2 to R1 (maximum degree), store result in R3
ADD R3, R1, R2

; Check if R3 is less than or equal to 3 (the allowed maximum)
; by subtracting 3 from R3, storing the result in R4
SUB R4, R3, #3

; If R4 is positive or zero (R3 is less than or equal to 3),
; then TST will set the ZERO PSR flag to 1
; Since we cannot use R4 twice in an instruction, we use R5 as an intermediate register
MOV R5, R4
TST R5, R4



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

