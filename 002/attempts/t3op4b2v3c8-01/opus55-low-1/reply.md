**Approach.** There are no sync points, so any interleaving that keeps each thread's own order is allowed. I first work out which values each block can hold, then which combinations of the three asked reads are possible.

**Values y can hold.**
- y starts at 0.
- B2 writes 2.
- C4 writes whatever C3 read from x. That read can be:
  - 0, if C3 comes before B1;
  - 3, written by B1;
  - the value A3 wrote, which is what A2 read from y.
- If C3 reads A3's value, then A2 came before A3, which came before C3, which came before C4. So A2 read y before C4 wrote, and A2 saw 0 or 2.
- So C4 writes 0, 2 or 3, and y only ever holds 0, 2 or 3.

**Q3, C1.** C1 comes before C4, so it sees only 0 or the 2 from B2. C1 ∈ {0, 2}.

**Q2, B3.** B3 comes after B2. It reads 2, or C4's value if C4 lands between B2 and B3.
- B3 = 0 is possible. It requires C3 before B1 and C4 between B2 and B3. Then C1 < C3 < B1 < B2, so C1 = 0.
  - In that run C4 writes 0, so y never holds 3. A1 can read 0 (before B2 or after C4) or 2 (between B2 and C4).
  - This gives (0,0,0) and (2,0,0).
- B3 = 3 is possible. It requires C3 after B1, so C4 writes 3.
  - A1 can read 0 if early, 2 after B2, or 3 after C4.
  - C1 can be 0, or 2 if placed after B2. For example: B1, B2, C1, C2, C3, C4, B3 works.
- B3 = 2 is possible. For example, all of B runs before C4, or C4 writes 2.
  - A1 can be 0, 2 or 3. For instance, C1 runs first, then all of B, then C3 reads 3, C4 writes 3, and A1 reads 3.
  - C1 can be 0 or 2.

BEGIN
0 0 0
2 0 0
0 2 0
0 2 2
2 2 0
2 2 2
3 2 0
3 2 2
0 3 0
0 3 2
2 3 0
2 3 2
3 3 0
3 3 2
END