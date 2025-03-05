{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if R0 <= 3 and R1 > 0
; Calculate R2 = R0 - 3
SUB R2, R0, #3

; Calculate R3 = R1 - 1
SUB R3, R1, #1

; Perform bitwise NOT on R2 and store in R4
MVN R4, R2

; Perform bitwise AND on R4 and R3, store in R5
AND R5, R4, R3

; Shift R5 left by 31 bits, store in R6
LSL R6, R5, #31

; Shift R6 right by 31 bits, store in R7
LSR R7, R6, #31

; Set APSR NZC flags based on R7
TST R7, #1



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

