{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Extract Width1 and Length1 from R0
MOV R2, R0, LSR #16 ; R2 = Width1
AND R3, R0, #65535  ; R3 = Length1

; Extract Width2 and Length2 from R1
MOV R4, R1, LSR #16 ; R4 = Width2
AND R5, R1, #65535  ; R5 = Length2

; Check if sum of widths <= 3 and sum of lengths <= 3
ADD R6, R2, R4      ; R6 = Width1 + Width2
ADD R7, R3, R5      ; R7 = Length1 + Length2

; Compare R6 and R7 with 3
CMP R6, #3          ; Compare Width1 + Width2 with 3
MVN R8, R6, LSL #31 ; If Width1 + Width2 > 3, R8 = 0, else R8 = 1

CMP R7, #3          ; Compare Length1 + Length2 with 3
MVN R9, R7, LSL #31 ; If Length1 + Length2 > 3, R9 = 0, else R9 = 1

; Check if both conditions are met
AND R10, R8, R9     ; R10 = R8 AND R9

; Set the ZERO PSR flag
TST R10, #1         ; Test if R10 equals 1



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

