{"register_size": 2}

;proof that Grover's Algorithm can be run with this!
;with register_size = 1, only X1X1 are measured
;hadamard
HAD R0

BAR

ORACLE
	MOV R0, #1
END_ORACLE

BAR

;takes the first bit from R0 and applies it to the target
MCT R0

REVERSE_ORACLE

;diffuser
DIF {R0}

STR CR0, R0
