**Approach.** First find every value each block can hold. Then decide which combinations of the asked values can happen together.

**Values block x can hold**
- B1 and C1 write 2.
- A5 writes whatever A3 read. B4 writes whatever B2 read.
- So x only ever holds 0 or 2. A4 can read 0 or 2.
- A3 reads 0 only if it takes effect before both B1 and C1.
- B2 takes effect after B1. So B2 reads 0 only in this order: B1, C1, then A5 writing 0, then B2. That needs A3 = 0.

**Values B5 can return**
- B5 comes after B3, so it returns either B3's value or C2's value of 1.
- C2's 1 is seen only if C2 takes effect between B3 and B5. Otherwise B5 returns what B2 read.
- So B5 is 1 if C2 falls between B3 and B5. Otherwise B5 equals what B2 read: 0 or 2.

**Case B2 = 0**
- The order is A3 = 0, then B1 and C1, then A5 writing 0, then B2, then B4 writing 0.
- After B4, no thread writes x again. So the final x is 0.
- B5 can be 0 or 1.
- A4 sits between A3 and A5. B1 or C1 can fall before or after it, so A4 can be 0 or 2.
- Final x = 2 is impossible here.

**Case B2 = 2**
- B5 can be 2 or 1.
- Final x can be 2, for example when B4 is the last write.
- Final x can be 0 when A3 reads 0 and A5 is the last write.
- A4 can be 0 or 2 with either final value:
  - A4 = 0 with final x = 2: A4 takes effect before both B1 and C1.
  - A4 = 2 with final x = 0: A4 reads after a write of 2, and A5 is still the last write.

**Result.** A4 can be 0 or 2 with each of these (B5, final x) pairs: (0, 0), (1, 0), (1, 2), (2, 0), (2, 2).

BEGIN
0 0 0
0 1 0
0 1 2
0 2 0
0 2 2
2 0 0
2 1 0
2 1 2
2 2 0
2 2 2
END