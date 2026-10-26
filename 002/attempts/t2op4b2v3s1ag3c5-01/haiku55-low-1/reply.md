**Setup.** Let a1…a4 and b1…b4 be the effect instants of the operations. Thread order gives a1 < a2 < a3 < a4 and b1 < b2 < b3 < b4. Because B1 and B2 finish before B3 starts, b2 < P. Because B4 starts after B3 ends, b4 > P. Because A4 starts after A3 ends and before P, a3 < P. The effect instants a4 and b3 can fall on either side of P.

**Final y (Q3).** The writes to y are a2 (value 2), b3 (value 3), and b4 (value v, where v is the value B1 read from x). Since a2 < a3 < P < b4 and b3 < b4, b4 is always the last write. So Q3 = v.

**B1 (v).** The writes to x are a1 (3) and a3 (1), and b1 < b2 < P. So v = 0 if b1 is before a1, v = 3 if a1 < b1 < a3, and v = 1 if b1 is after a3.

**B2 (Q2).** The only earlier write to y that can affect b2 is a2, since b3 and b4 come after b2. So Q2 = 2 if a2 < b2, and Q2 = 0 if b2 < a2. If Q2 = 0, then b1 < b2 < a2 < a3, so v ∈ {0, 3}.

**A4 (Q1).** a2 is always before a4. The last write to y before a4 is:
- 3 if b3 falls between a2 and a4 and b4 is after a4,
- v if b4 is before a4,
- 2 otherwise.

**Combinations.** Each combination below can be realized by choosing the placements of b1, b2, a2, a4, b3, and b4 relative to one another and to P, subject to the constraints above.

- Q2 = 2 (a2 < b2): v ∈ {0, 1, 3}. Q1 can be 2, 3, or v.
- Q2 = 0 (b2 < a2): v ∈ {0, 3}. Q1 can be 2, 3, or v.

That gives 13 combinations (Q1 Q2 Q3):

BEGIN
0 0 0
2 0 0
2 0 3
3 0 0
3 0 3
0 2 0
1 2 1
2 2 0
2 2 1
2 2 3
3 2 0
3 2 1
3 2 3
END