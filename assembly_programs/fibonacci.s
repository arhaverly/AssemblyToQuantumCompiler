{"register_size": 2, "decoding": {"CR0": "Fibonacci(0)", "CR1": "Fibonacci(1)", "CR2": "Fibonacci(2)", "CR3": "Fibonacci(3)", "CR4": "Fibonacci(4)"}}

MOV R0, #0       ; Initialize R0 with 0, F(0)
MOV R1, #1       ; Initialize R1 with 1, F(1)

; calculate F(2)
ADD R2, R0, R1   ; R2 = R0 + R1, calculate the next Fibonacci number (F(2))

; calculate F(3)
ADD R3, R1, R2   ; R3 = R1 + R2, calculate the next Fibonacci number (F(3))

; calculate F(4)
ADD R4, R2, R3   ; R4 = R2 + R3, calculate the next Fibonacci number (F(4))


; calculate F(5)
;ADD R5, R3, R4   ; R5 = R3 + R4, calculate the next Fibonacci number (F(5))


STR CR0, R0
STR CR1, R1
STR CR2, R2
STR CR3, R3
STR CR4, R4
