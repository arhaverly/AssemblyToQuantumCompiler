{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Initialize registers
MOV R2, #1 ; R2 = 1 (Subset {1})
MOV R3, #2 ; R3 = 2 (Subset {2})
MOV R4, #3 ; R4 = 3 (Subset {3})

; Check if R0 + R1 equals any subset sum
ADD R5, R0, R1 ; R5 = R0 + R1

; Compare R5 with subset sums
CMP R5, #0 ; Check if sum equals 0 (empty subset)
EOR R6, R5, R2 ; R6 = 0 if R5 matches R2 (Subset {1}), else non-zero
EOR R7, R5, R3 ; R7 = 0 if R5 matches R3 (Subset {2}), else non-zero
EOR R8, R5, R4 ; R8 = 0 if R5 matches R4 (Subset {3}), else non-zero

; Check if any subset sum is found
AND R9, R6, R7
AND R10, R8, R9
RSB R11, R10, #1 ; R11 = 1 if R10 is zero, else 0

; Set ZERO PSR flag
TST R11, #1 ; Sets ZERO flag if R11 contains 1, indicating a match found



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

