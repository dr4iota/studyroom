The possible outcomes are 13 combinations of (Q1, Q2, Q3), and the final answer block lists them.

**Constraints**

- Thread A's effects are ordered A1 < A2 < A3 < A4. A5 is irrelevant to the asked values.
- Thread B's effects are ordered B1 < B2 < B3 < B4 < B5. B4 takes effect before Q, and B5 takes effect after B4 and before P.
- A4 has no constraint relative to Q, so A's and B's operations can interleave freely within these chains.

**Value relations**

- rA1 (the value A1 reads) is the last y-write before A1, drawn from {0, 1 (B1), 3 (B2), rB3 (B4), 1 (B5)}. A2 and A4 come after A1, so they never affect it.
- rB3 (the value B3 reads) is the last y-write before B3, drawn from {3 (B2), rA1 (A2), 2 (A4)}, depending on whether A2 or A4 falls between B2 and B3.
- The final y is 1 if B5 is the last write, or 2 if A4 is the last write. A2 is always followed by A4, and B4 is always followed by B5, so neither can be last.

**Enumeration by where A1 falls**

- A1 before B1 gives rA1 = 0. Then rB3 can be 3, 0, or 2, and the final value can be 1 or 2 as allowed.
- A1 between B1 and B2 gives rA1 = 1. Then rB3 can be 3, 1, or 2.
- A1 between B2 and B4 gives rA1 = 3. Then rB3 can be 3 or 2.
- A1 between B4 and B5 gives rA1 = rB3 = 3.
- A1 after B5 gives rA1 = 1, rB3 = 3, and the final value is forced to 2.

Forcing rB3 = 2 means A4 lies between B2 and B3, so the final value is forced to 1.

BEGIN
0 3 1
0 3 2
0 0 1
0 0 2
0 2 1
1 3 1
1 3 2
1 1 1
1 1 2
1 2 1
3 3 1
3 3 2
3 2 1
END