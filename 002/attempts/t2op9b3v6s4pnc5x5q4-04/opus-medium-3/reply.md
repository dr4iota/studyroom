**Ordering constraints from the sync points**

- B1 < P < A3. A3 through A9 come after P.
- B1, B2 < Q < A9.
- A1 < S < B5. B5 through B9 come after S.
- All of A (A1–A9) < R < B8. So B8 and B9 come after every operation of A.

**z and B9**
- B8 is the last write to z, because it follows A1, A6 and A9, and B1 is earlier in B's own order.
- B9 comes right after B8, so B9 = final z = the value read by B2.

**y**
- Only A8 writes y, so final y = the value read by A7.
- A7 reads z right after A6 writes A4's value. No other write to z can fall between A6 and A7:
  - B1 is before P, so before A3.
  - A9 and B8 come later.
- So A7 = A4.
- A4 reads z after both A1 and B1 (since B1 < P < A3 < A4). It returns whichever of those two took effect later, so 6 or 1. Both orders are allowed.
- So final y ∈ {1, 6}.

**B2**
- B2 must be before Q, and A9 is after Q.
- A8 can be before or after B2. So B2 returns 0, or the value of y written by A8.

**x**
- B7 writes 4 last within B. So final x = 4, unless A2 takes effect after B7.
- A2 after B7 is possible: A1, then S, then B5–B7, then A2. In that case final x = 1.
- In that case, B2 < B5 < A2 < A8, so B2 must return 0.

**Combinations**
- x = 4:
  - B2 = 0: y = 1 or y = 6.
  - B2 = y: y = 1 (needs A1 < B1) or y = 6 (needs B1 < A1).
- x = 1: B2 = 0, with y = 1 or y = 6.

BEGIN
0 4 1 0
1 4 1 1
0 4 6 0
6 4 6 6
0 1 1 0
0 1 6 0
END