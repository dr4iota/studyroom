Taking each thread's constraints in turn, here is how the values narrow down.

**Constraints**
- B3 takes effect after P. B4 starts before Q and ends after Q, and it takes effect after B3.
- C1–C4 all end before Q.
- A3 reads 2, so the last write to x before A3 is a 2. A1, A2 and A3 are not otherwise constrained by P or Q.
- B2 reads y after B1 has written 1, so B2 returns 1 or 2, never 0. Call this value v. B3 and B4 both write v to x.

**Q3 (B2)**
- B2 = 1 requires B2 to take effect before C2.
- B2 = 2 requires C2 (or C4) to take effect first.
- Both are possible.

**Q1 (A1)**
- A1 = 0 works if A1 reads before C1 writes.
- A1 = 2 works if C1 has already written.
- A1 = 1 requires B3 to have taken effect, so v = 1 and B2 = 1. A3 still reads 2 only if C3 (which writes 2 to x) takes effect after B3 and before A3. Since B3 comes after B2, which comes after B1, and C2 comes before C3, this is consistent.

**Q2 (A2)**
- With A1 = 0 or 2, A2 can be 0 (before B1), 1 (after B1, before C2) or 2 (after C2). Every combination with B2 = 1 or 2 can be ordered consistently.
- With A1 = 1, B1 has already happened, so A2 cannot be 0. A2 can be 1 or 2, and B2 = 1.

That gives 2 × 3 × 2 = 12 combinations with A1 in {0, 2}, plus 2 combinations with A1 = 1.

BEGIN
0 0 1
0 0 2
0 1 1
0 1 2
0 2 1
0 2 2
2 0 1
2 0 2
2 1 1
2 1 2
2 2 1
2 2 2
1 1 1
1 2 1
END