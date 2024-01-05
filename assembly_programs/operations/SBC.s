{"register_size": 2, "run": true}


MOV R0, #3
ADC R1, R0, #0
;3 - 1 + Carry - 1 = 2
SBC R2, R0, #1


STR CR0, R2


