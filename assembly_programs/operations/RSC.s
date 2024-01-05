{"register_size": 2, "run": true}


MOV R1, #1
ADC R2, R1, #3
; 3 - 1 + Carry - 1 = 2
RSC R3, R1, #3


STR CR1, R3


