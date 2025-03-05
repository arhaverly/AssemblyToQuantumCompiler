{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Let R0 represent the number of unique registers required, and R1 represent the number of available registers.
; We want to check if R1 >= R0, and set the ZERO PSR flag accordingly.

; Store the difference between R0 and R1 in R2
SUB R2, R1, R0

; Perform a bitwise AND of R2 with the sign bit (0x80000000) in R3
MOV R3, #2147483648      ; Load immediate value 0x80000000 (2147483648 in decimal) into R3
AND R4, R3, R2           ; R4 = R3 AND R2

; Set ZERO PSR flag based on the result of AND operation
CMP R4, #0               ; Compare R4 with 0
; ZERO flag is now set to 1 if R4 == 0 (meaning R1 >= R0), otherwise it is set to 0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

