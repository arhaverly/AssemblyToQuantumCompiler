{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; R0 contains the binary representation of set A, where each bit represents an element
; R1 contains the binary representation of set B, where each bit represents an element

; Combine the sets using ORR to get the union of the sets
ORR R2, R0, R1

; Check if the union contains all elements from 1 to 3
; Since the largest number is 3, we check if the binary representation is 111
; (7 in decimal) using the CMP instruction
CMP R2, #7

; If the union is equal to 111, set the ZERO flag
; Use SUB with R3 to set the ZERO flag
; R3 is not relevant here, it's just used to set the flag
SUB R3, R2, #7

; Now, we need to set the ZERO PSR flag using the result in R3
; We can use the TEQ instruction to test R3 against 0
; If R3 is 0, it means the union is 111 and the ZERO flag will be set
TEQ R3, #0



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

