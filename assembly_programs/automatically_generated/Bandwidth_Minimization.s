{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; R2 = R0 + R1
ADD R2, R0, R1

; R3 = 3 - R2
; If R3 >= 0, then R0 + R1 <= 3, and thus the solution is valid.
RSB R3, R2, #3

; Set the ZERO PSR flag based on the comparison result
; If R3 >= 0, the ZERO flag will be set to 1, indicating a valid solution.
; Otherwise, the ZERO flag will be set to 0, indicating an invalid solution.
CMP R3, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

