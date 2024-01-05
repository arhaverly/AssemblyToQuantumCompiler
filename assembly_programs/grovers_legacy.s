{"register_size": 2}

;proof that Grover's Algorithm can be run with this!
;with register_size = 1, only X1X1 are measured
;hadamard
HAD R1
HAD R2

AND R3, R1, R2

;takes the first bit from R1 and applies it to the target
TGT R3

;need to remove once the reverse functionality is added
AND R3, R1, R2

;diffuser
DIF {R1, R2}

STR CR1, R1
STR CR2, R2
