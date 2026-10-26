Possible combinations are listed below. Each is checked against the sync-free ordering rules.

**Q3 (C4):** The only writes to y are B5 (value 2) and C5 (value 1). C5 comes after C4 in thread C, so C4 cannot return 1. C4 returns 0 or 2. Both are achievable, because B1 returning 0 only requires B1 to come before the first y write.

**Q1 (A1):** The writes to x that A1 could see are 0 (the initial value), 2 (from B2, B4 or C1) and 3 (from B3). So A1 returns 0, 2 or 3.

**Q2 (C2):** C1 writes 2 before C2, so C2 can return 2, or 3 if B3 lands in between. C2 can return 0 only if A5 writes 0 after C1 and before C2, which requires A1=0. A5 comes after A3, and that works because A3 can read 2 from C1 before A5 writes.
- A1=0: C2 can be 0, 2 or 3.
- A1=2 or A1=3: A5 writes 2 or 3, so C2 cannot be 0. C2 can be 2 or 3.

Each of these combines freely with C4 = 0 or 2. For A1=3, A3 reads 2 after B4 or C1 has written 2 following B3. For C4=2, B5 only needs to occur before C4, which is consistent with all of the above.

That gives 3 × 2 combinations for A1=0, and 2 × 2 combinations each for A1=2 and A1=3, so 14 in total.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 3 0
0 3 2
2 2 0
2 2 2
2 3 0
2 3 2
3 2 0
3 2 2
3 3 0
3 3 2
END