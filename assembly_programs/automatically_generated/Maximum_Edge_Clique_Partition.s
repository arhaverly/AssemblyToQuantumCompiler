{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; R0 and R1 contain the input values
; R2 will be used to store the result of the comparison

; Calculate the sum of R0 and R1
ADD R2, R0, R1

; Compare the sum to 6
CMP R2, #6

; Set the ZERO flag if the sum is equal to 6
; The result is stored in the APSR flags
; APSR.NZCV = R2 - 6
; Z flag will be set to 1 if R2 - 6 = 0 (i.e., R2 = 6)
; Otherwise, Z flag will be set to 0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

