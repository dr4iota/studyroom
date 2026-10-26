Every combination below can occur. I did not run a program; I reasoned from the ordering constraints.

**Ordering constraints**
- A1, A2 and A3 all take effect before P, in that order.
- B1 < B2 < B3 in effect order. B3 starts before P but ends after P, so its effect can fall before or after P. B4 starts after P, so it takes effect after A3.
- C1 < C2 < C3 < C4, and all of C finishes before Q.
- y receives B1 (value 1), C2 (value 2) and C4 (value 2). B1 can fall anywhere relative to C2 and C4, so B2 reads 1 or 2.
- B3 and B4 write B2's value to x, so x receives 1 only if B2 = 1.
- A3 = 2 only needs a write of 2 to x (C1 or C3) before A3, with no later write of another value. This can always be arranged.

**Case analysis**
- **B2:** it is 1 or 2.
- **A1:** it reads 0 (before C1), 2 (after C1), or 1. A1 = 1 requires B3 to take effect before A1 with B2 = 1, so A1 = 1 never occurs with B2 = 2.
- **A2 = 0:** A2 happens before B1 and C2. B3 comes after A1, so A1 ∈ {0, 2}. B2 can be 1 or 2. This gives (0,0,1), (0,0,2), (2,0,1), (2,0,2).
- **A2 = 1:** B1 comes before A2 and C2 comes after A2.
  - B2 = 1 works with A1 ∈ {0, 1, 2}. A1 = 1 needs B3 before A1, with C1 or C3 overwriting x afterwards.
  - B2 = 2 needs C2 before B2. Then A1 comes before C2, so A1 ∈ {0, 2}.
  - This gives (0,1,1), (1,1,1), (2,1,1), (0,1,2), (2,1,2).
- **A2 = 2:** C2 or C4 comes before A2.
  - A1 = 0 and A1 = 2 each work with B2 = 1 or B2 = 2.
  - A1 = 1 works only with B2 = 1. One ordering is C2 < B1 < B2 < B3 < A1 < A2, with C3 and C4 placed so that A3 still reads 2.
  - This gives (0,2,1), (0,2,2), (1,2,1), (2,2,1), (2,2,2).

BEGIN
0 0 1
0 0 2
2 0 1
2 0 2
0 1 1
1 1 1
2 1 1
0 1 2
2 1 2
0 2 1
0 2 2
1 2 1
2 2 1
2 2 2
END