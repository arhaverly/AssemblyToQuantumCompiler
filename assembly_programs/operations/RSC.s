{"register_size": 2, "run": true}


MOV R0, #1
ADC R1, R0, #3
; 3 - 1 + Carry - 1 = 2
RSC R2, R0, #3


STR CR0, R2


