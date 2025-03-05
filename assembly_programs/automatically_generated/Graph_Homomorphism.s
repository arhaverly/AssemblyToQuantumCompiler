{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; XOR R0 and R1, and store the result in R2
EOR R2, R0, R1

; Check if R2 is zero, and set the ZERO flag accordingly
; If R2 is zero, it means R0 and R1 are the same, which is not a valid solution
TEQ R2, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

