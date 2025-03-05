{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

    ; Check if R0 (number of routers) is greater than 0
    CMP R0, #1
    ; If R0 >= 1, result is 1, else result is 0
    MOV R2, #1
    CMN R0, #1
    MOV R3, #0
    EOR R2, R2, R3

    ; Check if R1 (number of switches) is greater than 0
    CMP R1, #1
    ; If R1 >= 1, result is 1, else result is 0
    MOV R3, #1
    CMN R1, #1
    MOV R4, #0
    EOR R3, R3, R4

    ; Combine the results of R2 and R3 using AND operation
    AND R5, R2, R3

    ; Set the ZERO PSR flag based on the result in R5
    TST R5, #1


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

