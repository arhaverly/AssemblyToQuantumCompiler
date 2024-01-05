{"register_size": 2}

MOV R1, #0       ; Initialize R1 with 0, F(0)
MOV R2, #1       ; Initialize R2 with 1, F(1)

; calculate F(2)
ADD R3, R1, R2   ; R3 = R1 + R2, calculate the next Fibonacci number (F(2))

; calculate F(3)
ADD R4, R2, R3   ; R4 = R2 + R3, calculate the next Fibonacci number (F(3))

; calculate F(4)
ADD R5, R3, R4   ; R5 = R3 + R4, calculate the next Fibonacci number (F(4))


; calculate F(5)
;ADD R6, R4, R5   ; R6 = R4 + R5, calculate the next Fibonacci number (F(5))


STR CR1, R5
