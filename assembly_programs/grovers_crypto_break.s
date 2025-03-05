{"register_size": 2, "run": true}



; R0 XOR R2. if R0 == 0b11 and R2 == 0b01, then R0 XOR R2 = 0b10, which equals the target


; R0 = key
HAD R0

; R1 = target
MOV R1, #2

; R2 = cypher
MOV R2, #1


ORACLE

	; decypher
	EOR R3, R0, R2

	; compare decypher to target
	CMP R1, R3

END_ORACLE


TGT ZERO

REVERSE_ORACLE

DIF {R0}

STR CR0, R0



