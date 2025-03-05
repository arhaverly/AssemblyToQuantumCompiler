{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

; Check if R0 is within the range [0, 3]
MOV R2, #3          ; Load immediate value 3 to R2
CMP R0, R2          ; Compare R0 with R2
RSB R3, R0, R2      ; Calculate R3 = R2 - R0
TST R0, R3          ; Test if R0 is within the range

; Check if R1 is within the range [0, 3]
MOV R4, #3          ; Load immediate value 3 to R4
CMP R1, R4          ; Compare R1 with R4
RSB R5, R1, R4      ; Calculate R5 = R4 - R1
TST R1, R5          ; Test if R1 is within the range

; Combine the results from R3 and R5 by setting the ZERO PSR flag
TEQ R3, R5          ; Test if both R0 and R1 are within the range


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

