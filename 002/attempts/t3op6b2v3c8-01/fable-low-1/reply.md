All x values are 0 or 2 (writes are 2 or copies of earlier reads), and y can end up 0, 1, or 2 before B5. Each combination is realizable:

- A4 = 0 if A's reads happen before any write; 2 otherwise.
- B5 = 2 (B3 writes 2 last), 1 (C2 last), or 0 (A5 writes 0 between B1 and B2, so B3 writes 0 last, with C2 before it).
- Final x = 0 if A5 or B4 writes 0 last; 2 otherwise.

BEGIN
0 0 0
0 0 2
0 1 0
0 1 2
0 2 0
0 2 2
2 0 0
2 0 2
2 1 0
2 1 2
2 2 0
2 2 2
END