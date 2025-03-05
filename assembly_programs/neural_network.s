{"register_size": 4, "run": false, "decoding": {"CR0": "weight", "CR1": "bias"}}


; R0 = weight
HAD R0

; R1 = bias
HAD R1


; R2 = input
MOV R2, #1

; R3 = target
MOV R3, #2


ORACLE

	; Forward propagate: output = input * weight + bias
	; correct weight and bias combinations:
	; weight = 1, bias = 1
	; weight = 0, bias = 2
	; weight = -1, bias = 3
	; weight = 2, bias = 0
	; etc.

	MUL R4, R0, R2
	ADD R5, R4, R1


	; compare output to target
	CMP R5, R3

END_ORACLE


TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1


