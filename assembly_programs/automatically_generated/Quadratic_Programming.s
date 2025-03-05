{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Calculate a * x^2
MOV R2, R0      ; R2 = x
LSL R3, R2, #1   ; R3 = x * 2
AND R4, R3, #3   ; R4 = (x * 2) AND 3, to make sure it's within the range [0, 3]
MOV R5, R1      ; R5 = a * b * c
AND R6, R5, #3   ; R6 = (a * b * c) AND 3, again to ensure it's within the range [0, 3]
ADD R7, R4, R6   ; R7 = (x * 2) AND 3 + (a * b * c) AND 3

; Check if the result is a multiple of 3
TST R7, #3       ; Test if R7 AND 3 == 0 (i.e., R7 is a multiple of 3)


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

