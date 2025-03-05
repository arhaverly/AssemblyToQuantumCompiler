{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Load the values in R0 and R1 into R2 and R3 respectively
MOV R2, R0
MOV R3, R1

; Calculate the sum of R2 and R3 and store it in R4
ADD R4, R2, R3

; Perform bitwise AND operation with 1 to check if the sum is even
; If the result is 0, the sum is even and the ZERO PSR flag is set to 1
; If the result is not 0, the sum is odd and the ZERO PSR flag is set to 0
AND R5, R4, #1
TEQ R5, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

