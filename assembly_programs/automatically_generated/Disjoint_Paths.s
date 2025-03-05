{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

; Let R0 and R1 represent two binary numbers, with each bit representing a path.
; Disjoint Paths problem: Check if there are no common paths (bits) between R0 and R1.
; For this example, let's assume the largest number allowed is 3 (binary representation: 00, 01, 10, 11).

; First, perform bitwise AND operation on R0 and R1 to find common paths.
AND R2, R0, R1

; Now, compare the result (R2) with 0.
; If R2 equals 0, then R0 and R1 have no common paths, and we set the ZERO PSR flag to 1.
; Otherwise, we set the ZERO PSR flag to 0.
TEQ R2, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

