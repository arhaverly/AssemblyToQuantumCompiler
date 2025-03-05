{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; R0 holds the number of vertices
; R1 holds the number of edges

; Check if the number of edges is less than the number of vertices
SUB  R2, R0, R1 ; R2 = R0 - R1

; Set the ZERO PSR flag to 1 if R2 is greater than 0 (R0 > R1)
; Set the ZERO PSR flag to 0 if R2 is less than or equal to 0 (R0 <= R1)
CMP  R2, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

