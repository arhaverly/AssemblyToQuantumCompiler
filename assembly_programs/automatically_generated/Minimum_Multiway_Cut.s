{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Assume R0 and R1 contain the values (edges weights) that cannot be changed
; Let's represent the Minimum Multiway Cut problem as finding if the sum of R0 and R1 is less than or equal to 3
; We will store the result in the ZERO PSR flag, 1 for a valid solution, 0 for not a solution

; Add the values of R0 and R1, storing the result in R2
ADD R2, R0, R1

; Subtract 4 from R2, storing the result in R3
SUB R3, R2, #4

; Perform a test for R3 with 0, setting the ZERO flag if equal (sum <= 3)
TST R3, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

