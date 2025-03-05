{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Store the sum of R0 and R1 in R2
ADD R2, R0, R1

; Check if the sum is even by ANDing with 1 and store the result in R3
AND R3, R2, #1

; Subtract R3 from 1 and store the result in R4
RSB R4, R3, #1

; Shift R2 right by 1 bit to divide it by 2 and store the result in R5
LSR R5, R2, #1

; Compare R5 with R0 to set the ZERO PSR flag
CMP R0, R5



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

