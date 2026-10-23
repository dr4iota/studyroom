All 12 combinations are possible: the first read A1 can return 0 or 4, and the reads B2 and B3 can return any non-decreasing pair from 0, 3, 4.

**Fixed orderings**
- **A3 needs B1 first.** A3 is known to return 4, and B1 is the only write of 4 to y. So B1 takes effect before A3.
- **Order of writes to z.** A2 (writes 3) takes effect before A4 (writes 4). B5 (writes 1) comes after B3 in thread B's program order. So while B2 and B3 run, z can only go 0 → 3 → 4.
- **B3 cannot see the value 1.** It follows from the previous point.

**A1 (Q1)**
- A1 returns 0 if it takes effect before B1.
- A1 returns 4 if it takes effect after B1.
- Either is allowed, because the only requirement is that B1 comes before A3.

**B2 and B3 (Q2, Q3)**
- B2 comes before B3, and z only increases through 0, 3, 4 during that time. So B3's value is never smaller than B2's.
- The possible pairs are (0,0), (0,3), (0,4), (3,3), (3,4) and (4,4).

**Combining the two**
- B2 and B3 only need to come after B1. A1 places no limit on where they fall relative to A2 and A4.
- **A1 = 0 with B2 = 0:** use the order A1, B1, B2, A2, …
- **A1 = 4 with B2 = 0:** use the order B1, A1, B2, A2, …
- **Larger B2 and B3 values:** delay B2 and B3 past A2 or A4 as needed.

So every pairing of an A1 value with a (B2, B3) pair is possible.

BEGIN
0 0 0
0 0 3
0 0 4
0 3 3
0 3 4
0 4 4
4 0 0
4 0 3
4 0 4
4 3 3
4 3 4
4 4 4
END