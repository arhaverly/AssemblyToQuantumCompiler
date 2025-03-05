{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

; Assume R0 and R1 store the values that represent the sizes of the two groups.
; If the difference between R0 and R1 is less than or equal to 1, they form a valid solution.
; We will store the result in the ZERO PSR flag.

; Step 1: Calculate the absolute difference between R0 and R1.
SUB R2, R0, R1 ; R2 = R0 - R1
RSB R3, R1, R0 ; R3 = R1 - R0
AND R4, R2, R3 ; R4 = min(R2, R3)

; Step 2: Compare the result with 1.
CMP R4, #1

; Step 3: Set the ZERO PSR flag to 1 if the difference is less than or equal to 1.
; Since the ZERO flag is set by the CMP instruction, we don't need to set it explicitly.



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

