{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Calculate the sum of vertices in the two induced subgraphs (forests) and store in R2
ADD R2, R0, R1

; Check if R2 is equal to 3 (total number of vertices)
CMP R2, #3

; Calculate the absolute difference between R0 and R1 and store in R3
RSB R3, R0, R1
CMP R3, #0
RSB R3, R3, #0

; Check if the absolute difference between R0 and R1 is greater than or equal to 2
CMP R3, #2

; Set the ZERO PSR flag to 1 if both conditions are met (R2 equals 3 and R3 >= 2)
TEQ R2, R3



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

