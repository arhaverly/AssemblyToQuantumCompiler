{"register_size": 4}

MOV R0 #5

;only one special register. for now...
;TODO also want it to match exactly
;register size must be > 4
MSR R0

STR CR0, R0
