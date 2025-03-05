{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if R0 - R1 = 3
SUB R2, R0, R1      ; R2 = R0 - R1
RSB R3, R1, R0      ; R3 = R1 - R0
CMP R2, #3          ; Compare R2 with 3
CMN R3, #3          ; Compare R3 with -3 (which is same as R0 - R1 = 3)
EOR R4, R2, R3      ; R4 = R2 XOR R3, R4 will be non-zero if R2 or R3 is non-zero
TST R4, #-1         ; Test R4 with -1 (all 1s in binary), sets ZERO flag if R4 is non-zero



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

