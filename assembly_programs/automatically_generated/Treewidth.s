{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; Load the value 3 into R2
MOV R2, #3

; Perform R2 - R0 and store the result in R3
SUB R3, R2, R0

; Perform R3 - R1 and store the result in R4
SUB R4, R3, R1

; Perform a bitwise AND between R4 and the sign bit (0x80000000) and store the result in R5
AND R5, R4, #2147483648

; Perform a bitwise AND between R4 and 0x7FFFFFFF (to only keep positive values) and store the result in R6
AND R6, R4, #2147483647

; Perform a bitwise OR between R5 and R6 and store the result in R7
ORR R7, R5, R6

; Check if R7 is equal to R4 and set the ZERO flag accordingly
TEQ R7, R4



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

