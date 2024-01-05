{"register_size": 4}

MOV R1 #5

;only one special register. for now...
;TODO also want it to match exactly
;register size must be > 4
MSR R1

STR CR1, R1
