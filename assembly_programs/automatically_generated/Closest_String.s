{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Step 1: Find XOR between R0 and R1, store the result in R2
EOR R2, R0, R1

; Step 2: Find if the XOR result has at most one bit set
; (i.e., R2 is one of 0, 1, 2, 4)

; Shift R2 right by 1 bit, store the result in R3
LSR R3, R2, 1

; Subtract R2 from R3, store the result in R4
SUB R4, R3, R2

; Test if the result is 1, 2 or 3 (i.e., at most one bit set in R2)
TST R4, 3

; Set the ZERO flag if the Hamming distance is at most 1
; Otherwise, keep it unset (default value 0)
; The ZERO flag will be set if the TST instruction has a zero result.



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

