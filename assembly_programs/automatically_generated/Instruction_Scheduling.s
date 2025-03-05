{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Calculate the difference between R0 and R1:
SUB R2, R0, R1 ; R2 = R0 - R1

; Calculate the absolute value of the difference:
RSB R3, R2, #0 ; R3 = -R2 (if R2 is positive, R3 becomes negative)
CMP R2, #0 ; Compare R2 with 0
EOR R4, R2, R3 ; If R2 is positive, R4 = R2 XOR R3; if R2 is negative, R4 = R2 XOR R2
AND R2, R4, R3 ; If R2 is positive, R2 = R4 AND R3 (keep R4); if R2 is negative, R2 = R4 AND R4 (keep 0)

; Check if the absolute difference is less than or equal to 1:
SUB R3, R2, #1 ; R3 = R2 - 1
TST R3, #2 ; Test if R3 has the 2 bit set (i.e., if R3 >= 2)
; The result of the TST instruction sets the ZERO PSR flag
; If the ZERO flag is set, R2 is a valid solution (difference <= 1)
; If the ZERO flag is not set, R2 is not a valid solution (difference > 1)



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

