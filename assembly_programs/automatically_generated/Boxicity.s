{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Move R0 into R2 and R1 into R3 to avoid reusing registers
MOV R2, R0
MOV R3, R1

; Perform XOR operation to find the difference in dimensions
EOR R4, R2, R3

; Move the result of XOR operation to R5
MOV R5, R4

; Test the difference and set the ZERO PSR flag accordingly
TST R5, R4



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

