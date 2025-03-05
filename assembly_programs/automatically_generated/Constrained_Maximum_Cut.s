{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Check if each element (0, 1, or 2) is in either R0 or R1 (but not both).
TST R0, R1         ; bitwise AND of R0 and R1, sets ZERO flag if none of the bits are the same
MOV R2, R0         ; copy R0 to R2 because registers can only be used once
ORR R3, R2, R1     ; bitwise OR of R2 and R1, now R3 should have all the bits set (111)

; Check if the sum of elements in R0 and R1 equals 3.
MOV R4, #7         ; 7 in binary is 111, which has 3 bits set
CMP R3, R4         ; compare R3 and R4, sets ZERO flag if they are equal

; Set the ZERO PSR flag based on the results.
AND R5, R0, R1     ; if R0 and R1 have no common bits, R5 will be 0
TEQ R5, #0         ; sets ZERO flag if R5 is 0
EOR R6, R0, R1     ; XOR of R0 and R1, should be 111 (7) if they are a valid solution
TEQ R6, R4         ; sets ZERO flag if R6 and R4 are equal
AND R7, R5, R6     ; if R5 and R6 are both 0, R7 will be 0
TEQ R7, #0         ; sets ZERO flag if R7 is 0, indicating a valid solution



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

