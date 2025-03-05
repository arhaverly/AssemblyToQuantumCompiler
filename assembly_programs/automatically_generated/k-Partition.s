{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Add R0 and R1, store the result in R2
ADD R2, R0, R1

; Check if the least significant bit of R2 is 0 (even)
; We do this using the AND instruction with 1
AND R3, R2, #1

; If R3 is 0, the sum is even, and we have a valid solution
; We'll store the result in the ZERO PSR flag by comparing
; R3 to 0 using the CMP instruction
CMP R3, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

