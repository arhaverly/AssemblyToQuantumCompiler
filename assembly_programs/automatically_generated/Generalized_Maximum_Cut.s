{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE


; R0 and R1 contain the two sets of nodes
; Use TST to set the ZERO PSR flag if bitwise AND of R0 and R1 is zero
TST R0, R1



END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

