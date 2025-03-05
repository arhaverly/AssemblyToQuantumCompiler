{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Load the maximum allowed number (3) into R2
MOV R2, #3

; Compare R0 and R1
CMP R0, R1

; If R0 <= R1, then R0 - R1 <= 0
; So, subtract R1 from R0 and store the result in R3
SUB R3, R0, R1

; Compare R0 and R2
CMP R0, R2

; If R0 <= R2, then R0 - R2 <= 0
; So, subtract R2 from R0 and store the result in R4
SUB R4, R0, R2

; Perform AND operation on R3 and R4
; If both R3 and R4 are <= 0, the result will be 0
AND R5, R3, R4

; Check if the result is 0
; If it is, the ZERO PSR flag will be set to 1
; Indicating that the values in R0 and R1 are a solution
CMP R5, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

