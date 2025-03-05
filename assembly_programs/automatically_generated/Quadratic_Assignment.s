{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Move the values from R0 and R1 to R2 and R3 for comparison
MOV R2, R0
MOV R3, R1

; Add the values in R2 and R3 and store the result in R4
ADD R4, R2, R3

; Check if the sum is equal to 10
MOV R5, #10
CMP R4, R5

; Use TEQ to set the ZERO PSR flag based on the comparison result
TEQ R4, R5

; The ZERO PSR flag is now set to 1 if the sum is equal to 10, and 0 otherwise.



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

