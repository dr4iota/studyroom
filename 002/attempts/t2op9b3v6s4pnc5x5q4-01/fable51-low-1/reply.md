**Analysis**

- B1–B6 happen before R and S; B7, B8 before P and Q; B9 is unconstrained.
- B2 reads y before any write to y can take effect (A4 is after S, hence after B6), so B2 = 0 → B8 writes 0 to y, B9 writes 0 to x.
- A1 reads y after Q (after B8), so A1 = 0 (irrelevant to the asked values).
- A3 reads x after B3 (x = 4); B9 may or may not have taken effect → A3 ∈ {4, 0}, written to y by A4.
- A5, A6, A8 each see x = 4 until B9 takes effect, then 0 forever: (4,4,4), (4,4,0), (4,0,0), (0,0,0).
- Final y: last writer among B4 (3), B8 (0), A4 (A3's value). B4 precedes both others, so final y ∈ {0, 4}; it is 4 only if A3 = 4 and A4 lands after B8, in which case B9 can still fall anywhere afterward, so all A5/A6/A8 patterns remain possible. Final y = 0 is also compatible with every pattern.

BEGIN
4 4 4 0
4 4 4 4
4 4 0 0
4 4 0 4
4 0 0 0
4 0 0 4
0 0 0 0
0 0 0 4
END