{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; R0 and R1 contain the lengths of subsequences
; R2 will hold the target length (3)
; R3 will hold the result of the comparison

; Load target length (3) into R2
MOV R2, #3

; Compare the sum of R0 and R1 to R2
ADD R3, R0, R1
CMP R3, R2

; Set ZERO flag based on the comparison
; Note: If the compared values are equal, the ZERO flag is set to 1, otherwise, it's set to 0
; Since the CMP instruction updates the ZERO flag automatically, we don't need to set it manually



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

