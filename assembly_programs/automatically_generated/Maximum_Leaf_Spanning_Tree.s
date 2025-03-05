{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Load immediate values into registers
MOV R2, #3         ; R2 = 3, total number of nodes in the largest tree
MOV R3, #1         ; R3 = 1, the root node that's not counted in the sum

; Calculate total nodes - 1 (root node)
SUB R4, R2, R3     ; R4 = R2 - R3, R4 = 2, expected sum for Maximum Leaf Spanning Tree

; Calculate the sum of nodes in R0 and R1
ADD R5, R0, R1     ; R5 = R0 + R1

; Compare the calculated sum with the expected sum
TST R5, R4         ; Perform bitwise AND between R5 and R4, set flags accordingly

; Set the ZERO PSR flag based on the comparison result
TEQ R5, R4         ; If R5 == R4, set ZERO PSR flag to 1, else it remains 0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

