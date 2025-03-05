{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Move the value of R0 into R2 and value of R1 into R3
MOV R2, R0
MOV R3, R1

; Add the values in R2 and R3 and store the result in R4
ADD R4, R2, R3

; Compare the value in R4 to 3
CMP R4, 3

; Set the ZERO flag if the values in R0 and R1 represent a valid solution
; (i.e., their sum is equal to 3)
; Since the ZERO PSR flag can only be set once, we will use the MRS and MSR instructions here
; to set the flag based on the comparison result.

; Save the current CPSR (flags) into R5
MRS R5, CPSR

; If the sum is equal to 3, the ZERO flag (Z) will be set.
; We will set the ZERO PSR flag to 1 if Z is set, and 0 if Z is not set.
; To do this, we will use the AND and ORR instructions with the appropriate masks.

; Mask for Z flag (bit position 30): 0b0100 0000 0000 0000 0000 0000 0000 0000 = 1073741824
MOV R6, 1073741824

; Check if Z flag is set in R5 and store the result in R7
AND R7, R5, R6

; If Z flag is set, R7 will be equal to the mask (1073741824), otherwise it will be 0
; Shift R7 right by 30 positions to get the required flag value (1 or 0)
LSR R7, R7, 30

; Clear the ZERO PSR flag in R5
BIC R5, R5, R6

; Set the ZERO PSR flag to the value in R7
ORR R5, R5, R7

; Update the CPSR (flags) with the new value in R5
MSR CPSR, R5



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

