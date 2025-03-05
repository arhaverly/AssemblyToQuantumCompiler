{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Extract node values and store them in R2-R5
AND R2, R0, #255         ; R2 = R0 & 0xFF
LSR R3, R0, #8           ; R3 = R0 >> 8
AND R6, R3, #255         ; R6 = R3 & 0xFF
LSR R4, R0, #16          ; R4 = R0 >> 16
AND R7, R4, #255         ; R7 = R4 & 0xFF
LSR R5, R0, #24          ; R5 = R0 >> 24

; Check if node values are unique
EOR R8, R2, R6           ; R8 = R2 ^ R6
EOR R9, R7, R5           ; R9 = R7 ^ R5
EOR R10, R8, R9          ; R10 = R8 ^ R9
CMP R10, #6              ; Compare R10 with 6 (0 ^ 1 ^ 2 ^ 3)
MOV R11, #1              ; R11 = 1
EOR R12, R11, R10, LSR #1; R12 = R11 ^ (R10 >> 1)
TST R12, #1              ; Test if R12 & 1 is non-zero (if R10 is even)

; Check if the ordering is valid
AND R13, R0, R1          ; R13 = R0 & R1 (bitmask of invalid edges)
TEQ R13, #0              ; Test if R13 == 0 (no invalid edges)

; Set the ZERO PSR flag
AND R14, R12, R13, LSR #1; R14 = R12 & (R13 >> 1)
TST R14, #1              ; Set the ZERO PSR flag



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

