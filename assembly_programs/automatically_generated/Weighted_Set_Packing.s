{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Add the values in R0 and R1, store the result in R2
ADD R2, R0, R1

; Check if the sum is equal to 3, store the result in the ZERO PSR flag
CMP R2, #3



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

