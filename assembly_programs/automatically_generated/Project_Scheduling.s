{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Initial values in R0 and R1 (assume they are given)
; R0 = number of tasks completed
; R1 = total number of tasks

; R2 will store the difference between R0 and R1
SUB R2, R1, R0

; Check if the difference is 0, if so, the project is complete
; Set the ZERO PSR flag accordingly
CMP R2, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

