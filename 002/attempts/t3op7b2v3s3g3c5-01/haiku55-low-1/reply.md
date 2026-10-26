I worked through the constraints by hand, and the result is 15 possible outcomes.

**Key facts:**
- All of B happens before P, and P < Q < R.
- Q3 (final y) is always the value read by A1. A5 is the last write to y, since it occurs after R and every other y-write precedes it.
- A1 reads x = 0 if it precedes B2, and 1 otherwise. So the A1 value, call it a, is 0 or 1.
- C1 reads v ∈ {0, 1} (its value is 0 before B2 and 1 after). Writes to y that can land before B6 and B7 are B1 (3), B5 (2), C2 (v), C3 (3), and C5 (3).
- B5 cannot fall between C3 and C4, or C4 would not read 3.
- B7 cannot read 2 unless B6 also reads 2.
- C7 reads 0 only if a = 0, or if v = 0 and the last write before C7 is C6.
- So the combination v = 1 with a = 1 is impossible.

**Feasible (Q1, Q2) pairs:** (2,2), (2,3), (2,v), (3,3), (v,v), (v,3). Each pair is then checked against the C7 constraint to pick the feasible Q3 values.

BEGIN
0 0 0
0 0 1
0 3 0
0 3 1
1 1 0
1 3 0
2 0 0
2 0 1
2 1 0
2 2 0
2 2 1
2 3 0
2 3 1
3 3 0
3 3 1
END