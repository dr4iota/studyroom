**Key constraints:** C2=1 forces A1 < C2 < A2, and C1 < C2, so A3 (after A2) always sees C1's write of 3 unless B4 overwrites x later. B5=1 is always satisfiable by placing C4 just before B5.

- B3 = 0 (before A1): A3 = 3, or 0 if B4 (writing 0) lands after C1 and before A3.
- B3 = 1 (between A1 and A2): A3 = 3, or 1 via B4.
- B3 = 2 (after A2): A3 = 3, or 2 via B4.
- A3 = 0 is impossible with B3 ∈ {1,2}, since A3 must follow C1 and B4 writes nonzero.

BEGIN
0 0
3 0
1 1
3 1
2 2
3 2
END