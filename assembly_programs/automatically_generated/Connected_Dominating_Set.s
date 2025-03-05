{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Ensure R0 is less than or equal to 3
MOV R2, #3
CMP R0, R2

; Ensure R1 is greater than 0
CMN R1, #1

; Combine the results using AND
AND R3, R2, R1

; Set the ZERO PSR flag based on the result in R3
TST R3, #1



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

