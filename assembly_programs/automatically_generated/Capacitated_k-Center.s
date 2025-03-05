{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

; Check if capacity (R0) is greater than 0
CMP R0, #1 ; compare R0 with 1
MOV R2, #0 ; set R2 to 0 (initialize)
CMN R0, #1 ; negate and compare R0 with 1
MVN R2, R2 ; negate R2 if R0 > 0

; Check if number of centers (R1) is greater than 0
CMP R1, #1 ; compare R1 with 1
MOV R3, #0 ; set R3 to 0 (initialize)
CMN R1, #1 ; negate and compare R1 with 1
MVN R3, R3 ; negate R3 if R1 > 0

; Combine the results
AND R4, R2, R3 ; R4 = R2 & R3

; Set ZERO flag
TST R4, #1 ; test R4 with 1, setting the ZERO flag according to the result


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

