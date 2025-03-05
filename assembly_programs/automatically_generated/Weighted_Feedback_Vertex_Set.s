{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Compute half of the total weight of vertices in the graph and store in R2
MOV R2, R0
LSR R2, R2, #1

; Subtract the total weight of vertices in the vertex set from half of total weight and store in R3
SUB R3, R2, R1

; Perform a comparison between R3 and 0
CMP R3, #0

; Set the ZERO PSR flag if the comparison results in equal or less than 0, otherwise clear the flag
RSB R4, R3, #0
ADD R5, R4, R3
TEQ R5, #0


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

