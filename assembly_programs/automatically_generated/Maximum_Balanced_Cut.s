{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if R0 and R1 differ by more than 1
SUB R2, R0, R1       ; R2 = R0 - R1
RSB R3, R2, #0       ; R3 = -R2
AND R4, R2, R3       ; R4 = R2 & R3, R4 is 0 if R2 and R3 have different signs (i.e., R0 and R1 differ by more than 1)

; Check if the total size is less than or equal to 3
ADD R5, R0, R1       ; R5 = R0 + R1
CMP R5, #3           ; Compare R5 with 3

; Set the ZERO PSR flag
MOV R8, #1           ; R8 = 1
TEQ R4, R8           ; Set ZERO PSR flag to 1 if R4 == R8, 0 otherwise



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

