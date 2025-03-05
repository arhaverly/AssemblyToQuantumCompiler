{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if R0 and R1 add up to 3

; Use R2 to store the value 3
MOV R2, #3

; Use R3 to store the sum of R0 and R1
ADD R3, R0, R1

; Compare the sum (R3) to 3 (R2)
CMP R3, R2

; Set ZERO flag to 1 if R3 == R2 (sum of R0 and R1 is 3)
; We use CMN instruction to achieve this
CMN R3, #3



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

