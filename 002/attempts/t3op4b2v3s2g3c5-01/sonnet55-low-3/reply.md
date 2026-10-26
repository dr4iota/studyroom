Every combination of (A1, A2, B2) that can occur is listed between BEGIN and END below.

**Constraints from the rules**
- All of A's steps happen before P.
- A3 returns 2, so the last write to x before A3 is a 2. That write comes from C1, C3, or B3 with the value 2.
- B3 starts before P and ends after P, so it may take effect on either side of P.
- B4 starts after P, so it takes effect after every A operation and cannot affect A's reads.
- B2 comes after B1 (y = 1), so it returns 1, or 2 if C2 took effect before it.

**Case B2 = 1**
- C2, C3 and C4 all take effect after B2.
- B3 writes 1 to x, and it can take effect before A1. Then A1 = 1, and C3 must write 2 to x before A3.
- A1 can be 0, 1 or 2.
- A2 can be 0, 1 or 2.
- If A1 = 1, then B1 precedes A1 and A1 precedes A2, so A2 cannot be 0.
- This gives 8 combinations.

**Case B2 = 2**
- C1 and C2 come before B2, and B3 and B4 write 2 to x, so x is never 1.
- A1 can be 0 (before C1) or 2.
- A2 can be 0 (before B1), 1 (between B1 and C2) or 2, with any A1 value.
- This gives 6 combinations.

BEGIN
0 0 1
0 1 1
0 2 1
1 1 1
1 2 1
2 0 1
2 1 1
2 2 1
0 0 2
0 1 2
0 2 2
2 0 2
2 1 2
2 2 2
END