Possible combinations (A3, C6): **(1, 4)** and **(5, 4)**.

**Step 1: B3 must return 4.**
- B2 returns 4 and is B's second operation, so it must read A4. B's own writes of y come after B2.
- So A1 → A4 → B2 → B3. B3 cannot read 1, because A4 has already overwritten A1's value.
- Suppose B3 returned 5. Then C1 must take effect between B2 and B3.
- C3 then reads 5 and C4 reads 4. That needs a write of 4 to y after C1. A4 is earlier than C1, and B4/B5 would write 5, so no such write exists.
- So B3 returns 4, and B4 and B5 write 4 to y.

**Step 2: A3 can only return 1 or 5.**
- A3 takes effect after A1 and before A4.
- B4 and B5 come after B2, which comes after A4, so A3 cannot see them.
- The only candidates are A1 (value 1) and C1 (value 5).

**Step 3: C6 must return 4.**
- C4 returns 4, so a write of 4 to y precedes C6.
- After that point, the only writes to y are A4, B4 and B5, and all of them write 4.
- A1 cannot be read here: if C4 read A4, A1 is earlier than A4. If C4 read B4 or B5, then A1 is earlier than B2.
- C1 cannot be read either: it must precede C3, which precedes C4.
- So C6 returns 4, and C8 writes 4 to z.

**Step 4: final z = 1.**
- The last write to z must write 1. C8 writes 4, C2 writes 4 and A5 writes 3.
- So the last write must be either B1, or A7 when A3 returned 1.

**Step 5: both values of A3 can be realised.**
- A3 = 1: run A1 and A3 before C1. Let the remaining A, B and C operations proceed with A7 as the last write to z. One such order is:
  1. C1, C2, C3
  2. A1, A2, A3 (reads 1), A4, A5, A6
  3. C4, C5, C6, C7, C8
  4. B1–B7
  5. A7

  All known read results hold in this order.
- A3 = 5: use this order:
  1. A1, C1, C2, C3, A2, A3 (reads 5)
  2. A4, A5, A6, A7
  3. C4–C8
  4. B1–B7

  B1 is the last write to z, so z ends at 1. B2, B3 and B7 read 4, and B6 reads x = 4.

BEGIN
1 4
5 4
END