Each operation takes effect at one instant, so every outcome comes from some total order of the six operations that keeps A1<A2<A3 and B1<B2<B3.

**B1.** B1 comes before B2 and B3, so it can only see 0 or A1's write. It returns 0 if it precedes A1 and 1 if it falls between A1 and B2.

**The writes.** B2 must come before B3, so the writes can occur in three orders:

1. A1, B2, B3. A2 and A3 come after A1, so each reads 1, 3 or 2, depending on whether it falls before B2, between B2 and B3, or after B3. They are non-decreasing in position, so the possible (A2, A3) pairs are (1,1), (1,3), (1,2), (3,3), (3,2), (2,2). B1 can be 0 (before A1) or 1 (between A1 and B2), independently of where the A reads fall.
2. B2, A1, B3. B1 must precede B2, so B1 = 0. The pairs are (3,3), (3,2), (2,2), which are already covered.
3. B2, B3, A1. B1 = 0 and both A reads return 1, giving (1,1), which is already covered.

The result is the six (A2, A3) pairs from order 1, each with B1 = 0 or 1.

BEGIN
1 1 0
1 1 1
1 3 0
1 3 1
1 2 0
1 2 1
3 3 0
3 3 1
3 2 0
3 2 1
2 2 0
2 2 1
END