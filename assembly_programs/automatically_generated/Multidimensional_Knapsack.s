{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Load the maximum allowed weight (3) into R2
MOV R2, #3

; Calculate R0 + R1 and store the result in R3
ADD R3, R0, R1

; Compare R3 with R2
CMP R3, R2

; Set the ZERO PSR flag based on the comparison result
; If R3 <= R2 (R0 + R1 <= 3), the flag is set to 1; otherwise, it's set to 0.
; To achieve this, we can use the EOR and TST instructions to set the ZERO PSR flag.

; Perform XOR operation between R3 and R2, save result in R4
EOR R4, R3, R2

; Perform bitwise AND operation between R3 and R4 to test the equality
TST R3, R4

; If R3 == R4, then the ZERO PSR flag will be set to 1, otherwise, it will be set to 0.



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

