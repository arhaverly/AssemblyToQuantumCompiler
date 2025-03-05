{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

; R2 temporary register
; Check if R0 = 3
MOV R2, #3
CMP R0, R2
; If R0 = 3, set R2 to 1 and perform AND with R1
; If R0 != 3, set R2 to 0
MOV R2, #1
SBC R2, R2, #0

; Check if R1 < 3
CMP R1, #3
; If R1 < 3, set R3 to 1 and perform AND with R2
; If R1 >= 3, set R3 to 0
MOV R3, #1
SBC R3, R3, #0

; Perform AND on R2 and R3 and store the result in R4
AND R4, R2, R3

; Check if R0 = 1 or R0 = 2
CMP R0, #1
; If R0 = 1, set R5 to 1
; If R0 != 1, set R5 to 0
MOV R5, #1
SBC R5, R5, #0

; Check if R0 = 2
CMP R0, #2
; If R0 = 2, set R6 to 1
; If R0 != 2, set R6 to 0
MOV R6, #1
SBC R6, R6, #0

; Perform ORR on R5 and R6 and store the result in R7
ORR R7, R5, R6

; Perform ORR on R7 and R4, and store the result in R8
ORR R8, R7, R4

; Set ZERO PSR flag to the value of R8
TST R8, #1


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

