{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if the incoming and outgoing flows are equal
SUB R2, R0, R1 ; R2 = R0 - R1

; Set APSR flags based on the result
CMP R2, #0 ; Compare R2 with 0

; Use EOR to determine if the values are the same
EOR R3, R2, #0 ; R3 = R2 XOR 0, if R2 is 0, R3 will be 0, otherwise, R3 will be non-zero

; Update the APSR flags based on R3
TST R3, #1 ; Test R3 with 1



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

