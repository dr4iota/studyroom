**Analysis**

- Final z / B9: B8 is after R, hence after all of A's ops, so B8 (value of B2) is the last write to z. Q1 = Q4 = value of B2.
- Final y: A8 is the only write to y, writing A7's value. A7 reads z after A6 (which rewrote A4's value), so A7 = A4. A4 sees either A1 (6) or B1 (1) last, both orders possible. Q3 ∈ {1, 6}.
- B2 reads y: either 0 (before A8) or A7's value (after A8, still before Q < A9).
- Final x: A2 (1) vs B7 (4) are unordered. If A2 is after B7, then B2 (earlier in B) precedes A8, forcing B2 = 0.

BEGIN
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
0 1 1 0
0 1 6 0
END