{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Let's assume that R0 and R1 store the values (jobs) assigned to two different machines (workers)
; R0 = Machine 1's job
; R1 = Machine 2's job
; Since the largest number allowed is 3, we have the following possible job pairs:
; (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), and (3, 2)

; We will first check if the jobs assigned to both machines are different
; We will use the EOR (exclusive OR) instruction. If the result is non-zero, 
; it means the jobs assigned are different, and thus the values in R0 and R1 are a valid solution

EOR R2, R0, R1 ; R2 = R0 XOR R1

; Now, we need to set the ZERO PSR flag to 1 if the values in R0 and R1 are a solution (R2 != 0) and 0 otherwise
; We will use the TST instruction to test if R2 is nonzero (R2 AND R2)

MOV R3, R2      ; Copy R2 to R3 to avoid using the same register twice in TST
TST R2, R3      ; Set ZERO flag if R2 == 0 (not a solution)



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

