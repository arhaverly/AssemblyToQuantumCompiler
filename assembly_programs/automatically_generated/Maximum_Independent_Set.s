{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

; Calculate bitwise OR of R0 and R1 to get complete adjacency matrix
ORR R2, R0, R1

; Check if A12, A13, and A23 are all 0 (independent set)
AND R3, R2, #7

; If R3 != 0, the ZERO flag is 0 (not a solution); otherwise, the ZERO flag is 1 (solution)
CMP R3, #0


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

