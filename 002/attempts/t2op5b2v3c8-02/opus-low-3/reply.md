I enumerated the possible interleavings, grouped by the value v that A1 reads. Without sync points, the only constraints are each thread's program order and the read-value rule.

**Constraints**
- Thread B's order fixes B1 (write 1) < B2 (write 3) < B3 < B4 in time.
- Thread A's order fixes A1 < A2 < A3 < A4. A4 writes v to x. A2 writes to y, which nobody reads, so it does not matter.
- B3 and B4 come after B2. Each returns 3, unless A4 (writing v) takes effect after B2 and before that read.
- So (B3, B4) can only be (3,3), (v,v) or (3,v). The pair (v,3) is impossible because no write of 3 happens after B2.
- A3 comes before A4, so A3 can only see B's writes, or 0 if none has happened yet.

**Case v = 0 (A1 before B1)**
- A3 can take effect before B1, between B1 and B2, or after B2. So A3 can return 0, 1 or 3.
- In each of these positions, A4 can still be placed before B2, between B2 and B3, between B3 and B4, or after B4. These give (3,3), (0,0), (3,0) and (3,3) respectively.
- So every A3 value combines with every one of those pairs. This holds even when A3 returns 3: A3 then falls after B2 but before B3, with A4 still before B3 or B4.

**Case v = 1 (A1 between B1 and B2)**
- A3 returns 1 if it takes effect before B2, or 3 if after.
- The same placements of A4 give (B3, B4) as (3,3), (1,1) or (3,1), for both values of A3.

**Case v = 3 (A1 after B2)**
- A3 must return 3.
- A4 writes 3, so B3 and B4 both return 3.

BEGIN
0 3 3
0 0 0
0 3 0
1 3 3
1 0 0
1 3 0
3 3 3
3 0 0
3 3 0
1 1 1
1 3 1
3 1 1
3 3 1
END