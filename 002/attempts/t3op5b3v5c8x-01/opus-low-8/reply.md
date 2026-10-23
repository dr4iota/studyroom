**Approach.** There are no sync points, so any interleaving that keeps each thread's own order is allowed. Let a be the value A1 reads from z and b the value B2 reads from x.

- **What A1 can read.** a can be 0, 1 or 2. a=1 needs B1 before A1, and a=2 needs C1 before A1.
- **What B2 can read.** b can be 0 or 1. b=1 needs C2 before B2.
- **Writes to z.** z receives the values 1 (B1), 2 (C1) and a (A2, A3).
- **Final y.** It is a if A4 is the later write to y, or b if B3 is the later one.

**Case a=0** (A1 runs before both B1 and C1). B5 and C4 can each see 0, 1 or 2.
- The pair (B5=2, C4=1) is impossible. C4 seeing 1 needs B1 after C1. Then B5, which comes after B1, could only see 2 if C1 came after B1, which contradicts it.
- The other 8 pairs work with y=0.
- y=1 needs b=1 (C2 before B2) and B3 after A4. This works for every pair except (2,0). For (2,0), B5 must see 2 and C4 must see 0. That forces B1 < C1 < C2 < B2 < B3 < B5, with an A write landing after B5 and before C4. But A4 must come before B3, and A2 and A3 come before A4, so no A write can land after B5.

**Case a=1** (B1 before A1). B5 and C4 can each see 1 or 2, and y is 0 or 1.
- The new combination here is (2,1,1). C4 sees 1, so an A write falls between C1 and C4. B5 sees 2, so B5 comes before A2, which means B3 comes before A4 and the final y is 1.

**Case a=2** (C1 before A1). B5 and C4 can each see 1 or 2, and y can be 0, 1 or 2.
- Each pair (1,1), (1,2), (2,1) and (2,2) can be paired with every value of y. For (1,2) with y equal to b: all A writes come before B1, and C4 comes before B1. For (2,1): B1 is the last write before C4, and an A write falls between B1 and B5.

**Result.**
- y=0 is possible for every pair except (2,1) from Case a=0. Case a=2 then supplies (2,1,0), so all 9 pairs work.
- y=1 is possible for all 9 pairs except (2,0).
- y=2 is possible only for pairs whose values are 1 or 2.

BEGIN
0 0 0
0 1 0
0 2 0
1 0 0
1 1 0
1 2 0
2 0 0
2 1 0
2 2 0
0 0 1
0 1 1
0 2 1
1 0 1
1 1 1
1 2 1
2 1 1
2 2 1
1 1 2
1 2 2
2 1 2
2 2 2
END