Every combination is possible except where A1 = 3 meets B3 = 0, C1 = 3, or (A1 = 3, B3 = 2, C1 = 2). This leaves 14 combinations.

**Which values can be written**
- Block y receives only two writes: B2 writes 2, and C4 writes whatever C3 read from x.
- Block x receives only two writes: B1 writes 3, and A3 writes whatever A2 read from y.
- C4's value can only come from 0, B1's 3, or A3's value. A3's value would have to come from 0, 2, or C4's own write, which is circular. So C4 writes 0, 2 or 3.
- Therefore every read of y returns 0, 2 or 3.

**Q3 (C1)**
- C1 runs before C4 in thread C, so it can only see 0 or B2's 2.
- C1 = 3 is impossible.

**Q2 (B3)**
- B3 runs after B2, so it returns 2 unless C4 overwrites y in between. In that case it returns C4's value: 0, 2 or 3.

**Q1 (A1)**
- A1 can return 0, 2 or 3.

**Combinations that cannot happen**
1. **A1 = 3 with B3 = 0.** The value 3 can reach y only through C4, and so can 0 once B2 has run. Both would need C4, which writes only one value.
2. **A1 = 3, B3 = 2, C1 = 2.** C4 must write 3, so B2 must come after C4 for B3 to read 2. But C1 = 2 needs B2 before C1, and C1 is before C4. These orders contradict each other.

**Combinations that can happen, with a witness order for each family**
- **B3 = 3:** C4 writes 3 between B2 and B3, and C3 reads x after B1. For example: B1, B2, C1, C2, C3 (reads 3), C4 (writes 3), A1, B3. Moving A1 or C1 earlier gives the other A1 and C1 values.
- **B3 = 2:** B3 runs right after B2 with no C4 write in between. A1 and C1 can each see 0 or 2. If C4 writes 3 before B2, A1 can see 3, but then C1 must be 0.
- **B3 = 0:** C4 writes 0 between B2 and B3.
  - C3 can read x = 0 before B1 runs.
  - Alternatively, A2 reads 0 before B2, and A3 writes that 0 to x after B1 but before C3. This allows C1 = 2.
  - A1 then returns 0 or 2.

BEGIN
0 0 0
0 0 2
2 0 0
2 0 2
0 2 0
0 2 2
2 2 0
2 2 2
3 2 0
0 3 0
0 3 2
2 3 0
2 3 2
3 3 0
3 3 2
END