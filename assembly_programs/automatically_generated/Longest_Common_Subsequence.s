{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if R0 and R1 are greater than or equal to 3 (the required longest common subsequence length)
SUB R2, R0, #3 ; R2 = R0 - 3
SUB R3, R1, #3 ; R3 = R1 - 3

; Compute the bitwise AND of the most significant bits (MSBs) of R2 and R3
; If both MSBs are 0, the result will be 0, indicating a valid solution
AND R4, R2, R3, LSR #31 ; R4 = (R2 >> 31) & (R3 >> 31)

; Set the ZERO PSR flag based on the result in R4
CMP R4, #0 ; Compare R4 with 0 and update the flags



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

