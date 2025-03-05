{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Initialize registers
MOV R2, #3      ; R2 = 3
MOV R3, #1      ; R3 = 1

; Add R0 and R1, store the result in R4
ADD R4, R0, R1  ; R4 = R0 + R1

; Compare the sum with 3 and set the APSR Z flag accordingly
CMP R4, R2      ; Compare R4 and R2, Z flag will be set if R4 == R2

; The ZERO (Z) flag in the APSR register is now set to 1 if R0 + R1 == 3, and 0 otherwise.



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

