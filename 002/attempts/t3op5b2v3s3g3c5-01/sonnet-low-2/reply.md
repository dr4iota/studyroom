Every combination below is possible.

**Constraints from the sync points**
- All of thread C finishes before P. B4 ends after P and spans Q, so B4 reads 2 after C's writes are done.
- B1 reads 0, so it takes effect before C1 (C1 is the first write to y that can precede it, and B3 comes after B1).
- A2 ends after R, and A3 and A5 come after A2. B1 is before R.
- y is written by C1 (1), C2 (2) and B3 (2), with C1 before C2.

**Possible histories of y**
- **B3 first (before C1):** y goes 0, 2, 1, 2. This is the only non-monotonic history. Here B2 must read 0, because B2 comes before B3 and C3 comes after C1. A5 could take effect early, but it still comes after B2 in the relevant case, so x is 0 at B2.
- **B3 later:** y goes 0, 1, 2, 2, which is monotonic.

**Pairs (A1, A2)**
- Under the non-monotonic history, A2 takes effect at or after A1, so the pairs are 00, 01, 02, 11, 12, 21, 22, all with B2 = 0.
- Under the monotonic history, the pairs are 00, 01, 02, 11, 12, 22. B2 can read 0, or 1 if C3 (or A5) has already written x. B3 then falls after C3, and A3 still reads 2 after C2.
- The pair 21 needs the non-monotonic history, so it only occurs with B2 = 0.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 1 0
1 1 1
1 2 0
1 2 1
2 1 0
2 2 0
2 2 1
END