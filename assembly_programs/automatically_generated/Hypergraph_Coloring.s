{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

; Compare R0 and R1 and set the ZERO flag accordingly
TEQ R0, R1 ; Compare R0 and R1; if R0 == R1, ZERO flag is set to 1, otherwise set to 0


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

