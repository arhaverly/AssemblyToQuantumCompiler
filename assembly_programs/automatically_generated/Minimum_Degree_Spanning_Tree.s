{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Assume R0 contains a value representing the total weight of the spanning tree
; Assume R1 contains a value representing the number of edges in the spanning tree
; For a graph with 3 nodes (largest number allowed), the minimum degree spanning tree
; should have a total weight of 3 and 2 edges connecting the nodes.

; Check if the total weight is 3 by comparing R0 with 3
MOV R2, #3      ; R2 = 3
CMP R0, R2      ; Compare R0 with R2 (3)

; If R0 is equal to 3, set R3 to 1, else set it to 0
MOV R3, #1      ; R3 = 1
MOV R4, #0      ; R4 = 0
EOR R3, R3, R4, LSR #1 ; R3 = R3 ^ (R4 > 0), if R0 == 3, R3 = 1, else R3 = 0

; Check if the number of edges is 2 by comparing R1 with 2
MOV R5, #2      ; R5 = 2
CMP R1, R5      ; Compare R1 with R5 (2)

; If R1 is equal to 2, set R6 to 1, else set it to 0
MOV R6, #1      ; R6 = 1
MOV R7, #0      ; R7 = 0
EOR R6, R6, R7, LSR #1 ; R6 = R6 ^ (R7 > 0), if R1 == 2, R6 = 1, else R6 = 0

; If both R3 and R6 are 1, the values in R0 and R1 are a valid solution
; to the Minimum Degree Spanning Tree problem
AND R8, R3, R6  ; R8 = R3 & R6, if R0 == 3 and R1 == 2, R8 = 1, else R8 = 0

; Set the ZERO PSR flag to the result in R8
CMP R8, #1      ; Compare R8 with 1, setting the ZERO PSR flag accordingly



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

