{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Representing the graph as adjacency matrix
; R0 = 011b = 3, R1 = 101b = 5
; Adjacency matrix:
; 0 1 1
; 1 0 1
; 1 1 0

; Check if both R0 and R1 have bits 1 and 2 set (excluding the diagonal)
; We need to check if R0 AND 6 = 6 and R1 AND 6 = 6

; Load the value 6 (110b) into R2
MOV R2, #6

; Perform bitwise AND between R0, R2 and store the result in R3
AND R3, R0, R2

; Perform bitwise AND between R1, R2 and store the result in R4
AND R4, R1, R2

; Check if R3 equals R2 (6) and store the result in R5
; If R3 equals R2, R5 will be 0
SUB R5, R3, R2

; Check if R4 equals R2 (6) and store the result in R6
; If R4 equals R2, R6 will be 0
SUB R6, R4, R2

; Now, if both R5 and R6 are 0, then the graph is a complete graph
; Perform bitwise OR between R5, R6 and store the result in R7
ORR R7, R5, R6

; If R7 is 0, it's a Hamiltonian cycle, otherwise it's not
; We can set the ZERO PSR flag by comparing R7 with 0 using CMP
CMP R7, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

