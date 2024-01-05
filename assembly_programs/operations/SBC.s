{"register_size": 2, "run": true}


MOV R1, #3
ADC R2, R1, #0
;3 - 1 + Carry - 1 = 2
SBC R3, R1, #1


STR CR1, R3


