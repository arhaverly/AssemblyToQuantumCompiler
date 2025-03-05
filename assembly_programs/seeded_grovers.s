{"register_size": 1, "run": true}


;1. 2 variables to optimize
;2. a seed

;I want to train these variables on the conditions set up by the seed. Essentially, I want to optimize the variables on all of the different conditions that the seed qubit can generate. Then I want to measure the optimized variables based on all of these different configurations.

;if seed == 0, i want to measure 10
;

;if seed == 1, i want to measure 11


; variables to optimize
HAD R0
HAD R1

; seed
HAD R2


ORACLE

	AND R3, R0, R2
	AND R4, R1, R2
	AND R5, R3, R4

END_ORACLE


TGT R5

REVERSE_ORACLE

DIF {R0, R1}
;DIF {R0, R1, R2}






STR CR0, R0
STR CR1, R1
;STR CR2, R2


