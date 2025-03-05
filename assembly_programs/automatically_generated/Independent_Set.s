{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if R0 and R1 have common nodes by performing a bitwise AND operation
AND R2, R0, R1 ; R2 = R0 & R1

; Move the value of R2 to R3
MOV R3, R2

; Check if R3 is zero
TST R2, R3 ; Set the ZERO flag if R3 == 0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

