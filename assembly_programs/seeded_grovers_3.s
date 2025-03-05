{"register_size": 1, "run": true}


;1. 2 variables to optimize
;2. a seed

;I want to train these variables on the conditions set up by the seed. Essentially, I want to optimize the variables on all of the different conditions that the seed qubit can generate. Then I want to measure the optimized variables based on all of these different configurations.


; variables to optimize
HAD R0
HAD R1
HAD R2

; seed
HAD R3


ORACLE

	AND R4, R0, R1
	AND R5, R2, R3
	AND R6, R4, R5

END_ORACLE


TGT R6

REVERSE_ORACLE

DIF {R0, R1, R2}

ORACLE

	AND R4, R0, R1
	AND R5, R2, R3
	AND R6, R4, R5

END_ORACLE


TGT R6

REVERSE_ORACLE

DIF {R0, R1, R2}


ORACLE

	AND R4, R0, R1
	AND R5, R2, R3
	AND R6, R4, R5

END_ORACLE


TGT R6

REVERSE_ORACLE

DIF {R0, R1, R2}




STR CR0, R0
STR CR1, R1
STR CR2, R2


