{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if R0 and R1 have a shared vertex (bitwise AND to find common bits)
AND R2, R0, R1
; Invert R2 to check for independence later
MVN R3, R2

; Create the union of R0 and R1 (bitwise OR)
ORR R4, R0, R1

; Check if the union covers all vertices (4 nodes, so the largest number allowed is 3)
; Create a mask with all bits set to 1 (3 = 0b11)
MOV R5, 3

; Check if the union equals the mask (bitwise XOR)
EOR R6, R4, R5

; Check if both sets are independent (R3 should have all bits set to 1)
; Check if R6 (result of XOR) and R3 (inverted AND) are the same (bitwise XOR)
EOR R7, R6, R3

; Check if R7 equals R5 (mask), which means it's a valid solution
; Set the ZERO PSR flag to 1 if R7 equals R5, otherwise set it to 0
TEQ R7, R5



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

