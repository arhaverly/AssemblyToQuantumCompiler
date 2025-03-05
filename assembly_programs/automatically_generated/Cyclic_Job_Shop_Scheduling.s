{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

    ; Check if R0 >= 1
    CMP R0, #1
    ; Perform R2 = R0 - 1
    SUB R2, R0, #1
    ; Check if R1 >= 1
    CMP R1, #1
    ; Perform R3 = R1 - 1
    SUB R3, R1, #1

    ; Check if R2 >= 0 and R3 >= 0
    ; If R0 >= 1 and R1 >= 1, R2 and R3 would be >= 0
    ; R4 = R2 AND R3
    AND R4, R2, R3

    ; Set ZERO flag based on R4 value
    ; If R4 >= 0, it means R0 >= 1 and R1 >= 1, making it a valid solution
    TEQ R4, #0


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

