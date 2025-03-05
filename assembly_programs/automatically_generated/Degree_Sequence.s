{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Let R0 = A, R1 = B
; We assume that A and B are non-negative integers. Since the largest number allowed is 3,
; possible values for A and B are {0, 1, 2, 3}. The valid pairs for Degree Sequence problem are:
; (0, 0), (1, 1), (2, 2), (3, 3)
; So, we have to check if A == B

; Load the difference A - B into R2
SUB R2, R0, R1

; Load the difference B - A into R3
SUB R3, R1, R0

; Perform a bitwise OR operation on R2 and R3, and store it in R4
ORR R4, R2, R3

; Perform a bitwise NOT operation on R4, and store it in R5
MVN R5, R4

; Perform a bitwise AND operation on R5 and 0x3 (since max value is 3), and store it in R6
AND R6, R5, #3

; If R6 is zero, then A and B are equal and we have a solution; otherwise, it's not a solution
; Set the ZERO PSR flag based on the value in R6
CMP R6, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

