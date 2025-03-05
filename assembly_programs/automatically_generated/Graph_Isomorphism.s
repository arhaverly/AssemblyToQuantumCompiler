{"register_size": 2, "run": false, "display": false}
HAD R0
HAD R1

ORACLE

  MOV R2, #7   ; Load immediate value 7 (0b111) in R2
  AND R3, R0, R2   ; Extract the adjacency matrix of G0 from R0
  LSR R0, R0, #3   ; Shift right R0 by 3 bits to extract the adjacency matrix of G1
  EOR R4, R3, R0   ; XOR the adjacency matrices of G0 and G1
  TST R4, R2   ; Check if the XOR result matches the adjacency matrix mask (0b111) and set the ZERO PSR flag


END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

