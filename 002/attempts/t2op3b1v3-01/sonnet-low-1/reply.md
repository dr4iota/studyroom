Thread A has no sync points, so any interleaving of the two threads is allowed. I enumerate by where A1 falls among B's writes.

**B1.** B1 comes before B2 and B3 in thread B, so it can never see 3 or 2. It returns 0 if it takes effect before A1, and 1 if it falls between A1 and B2. So B1 is 0 or 1.

**A2 and A3.** Both come after A1, so each sees A1's value or a later write. The write order and the reads each thread can see fall into three cases:

1. **Order A1, B2, B3.** The block goes 1, then 3, then 2. A2 and A3 are non-decreasing in time, giving (1,1), (1,3), (1,2), (3,3), (3,2), (2,2). B1 can be 0 (before A1) or 1 (between A1 and B2) with any of these six pairs.
2. **Order B2, A1, B3.** The block goes 3, then 1, then 2, so B1 sees 0. After A1 the reads give (1,1), (1,2), (2,2). These are already covered by case 1.
3. **Order B2, B3, A1.** The block goes 3, then 2, then 1, so B1 sees 0. Both reads give (1,1), already covered.

The union is the six (A2, A3) pairs from case 1, each with B1 equal to 0 or 1.

BEGIN
1 1 0
1 3 0
1 2 0
3 3 0
3 2 0
2 2 0
1 1 1
1 3 1
1 2 1
3 3 1
3 2 1
2 2 1
END