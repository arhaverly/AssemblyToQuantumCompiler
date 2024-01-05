{"register_size": 2}

;proof that Grover's Algorithm can be run with this!
;with register_size = 1, only X1X1 are measured
;hadamard
HAD R1

BAR

ORACLE
	MOV R1, #1
END_ORACLE

BAR

;takes the first bit from R1 and applies it to the target
MCT R1

REVERSE_ORACLE

;diffuser
DIF {R1}

STR CR1, R1
