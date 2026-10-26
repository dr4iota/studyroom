**Answer:** B2 always returns 2 and the final y is always 2. C4 can return 2 or 5, and the final z can be 2 or 4, in any pairing.

**Approach.** There are no sync points here. So every execution is one ordering of all the operations that keeps each thread's own order. Each read returns the latest earlier write to its block.

**1. What B1 must have read.** B5 reads z = 2. The only writes to z are A1 (3), A4 (4) and B3 (the value B1 read).
- So B3 is the last write to z before B5, and it wrote 2.
- That means B1 read y = 2.
- The writes to y are C1 (2) and B4 (B1's value). B4 comes after B1 in thread B, so B1 must come after C1.

**2. Q1 (B2).** B2 comes after B1, so it is also after C1. Every write to y writes 2, so B2 returns 2.

**3. Q3 (final y).** Every write to y writes 2, so the final y is 2. A2 reading 2 is consistent with this.

**4. Ordering the writes to z.** C2 reads z = 3, so A1 comes before C2, with no other write to z between them. There are two possible cases:
- **Case 1:** A1 < C2 < B3 < B5. A4 is not between B3 and B5. So A4 is either between C2 and B3, or after B5.
- **Case 2:** B3 < B5 < A1 < C2, with A4 after A1.

**5. Q4 (final z).**
- In Case 1 with A4 before B3, B3 is the last write, so z ends as 2.
- In Case 1 with A4 after B5, and in Case 2, A4 is the last write, so z ends as 4.

**6. Q2 (C4).** The writes to x are A3 (2) and C3 (5).
- If A3 falls between C3 and C4, C4 returns 2.
- Otherwise C4 returns 5.

Both placements of A3 work with either final value of z. These orderings show the cases where C4 returns 2:
- C1, A1, A2, C2, C3, A3, C4, B1, B2, B3, B4, B5, A4 gives C4 = 2 and final z = 4.
- C1, A1, A2, C2, C3, A3, C4, A4, B1, B2, B3, B4, B5 gives C4 = 2 and final z = 2.

Moving A3 before C3 in either ordering gives C4 = 5 with the same final z.

BEGIN
2 2 2 2
2 2 2 4
2 5 2 2
2 5 2 4
END