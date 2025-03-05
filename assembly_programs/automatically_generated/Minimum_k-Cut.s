{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Compare R0 and R1 (R0 - R1)
SUB R2, R0, R1

; If R2 is greater than 0, R1 < R0, not a solution
; If R2 is less than or equal to 0, R1 >= R0, valid solution
; Set ZERO PSR flag based on R2
RSB R3, R2, #0
TST R3, R2



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

