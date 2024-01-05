{"register_size": 2}

;proof that Grover's Algorithm can be run with this!
;with register_size = 1, only X1X1 are measured
;hadamard
HAD R0
HAD R1

AND R2, R0, R1

;takes the first bit from R0 and applies it to the target
TGT R2

;need to remove once the reverse functionality is added
AND R2, R0, R1

;diffuser
DIF {R0, R1}

STR CR0, R0
STR CR1, R1
