The possible outcomes are the 12 combinations of Q1 ∈ {0, 2}, Q2 ∈ {0, 2}, and Q3 ∈ {0, 2, 3}.

**Key facts:**
- Q1 is 2 if A1 takes effect before B1, and 0 otherwise. No other write to x can precede B1, since B4 comes after B1 in its thread.
- Q2 is the value of the later of A1 (writes 2) and B4 (writes the value of y at B2). That value is either 0 or the value C writes to y.
- Q3 is the value of the later of C1 (writes 3) and A4 (writes the value of y at A3).
- All values are in {0, 2, 3}. Only 2 and 0 propagate through x and y.

**Q1, Q2, and Y3 (the value of y at A3):** I checked all 8 combinations of (Q1, Q2, Y3) in {0,2}³ and found a schedule for each. For example, (0, 0, 2) comes from B1, A1, C1, C2, C3, B2, A3, B3, B4, C4, and (2, 2, 0) from A1, B1, A3, C1, C2, C3, B2, B3, B4, C4.

**Q3 = 0 or 2:** Place A4 last, after C1. Then Q3 equals Y3, so every (Q1, Q2) pair combines with Q3 ∈ {0, 2}.

**Q3 = 3:** Place A4 before C1. Each of the four (Q1, Q2) pairs has a schedule. For example, (2, 2, 3) comes from A1, B1, A2, A3, A4, C1, C2, C3, B2, B3, B4, C4, where C1 writes 3 to z after A4 has already written.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
END