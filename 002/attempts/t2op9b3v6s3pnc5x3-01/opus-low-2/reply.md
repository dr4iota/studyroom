**Answer:** A9 always returns 5. The final y can be 4 or 6, and the final z can be 4 or 6, in any combination.

**Ordering constraints from the sync points**
- B1–B3 happen before R, and A9 happens after R.
- B4 and B5 happen before P. A7 and A8 happen after P and before Q.
- B7–B9 happen after Q. B6 only has to come after B5.

**Q1: the value returned by A9**
- B8 runs after Q, which is after A8.
- The only other writes to x are B2 and B4, and both are before P. So the last write to x before B8 is A8's 5, and B8 reads 5.
- B9 therefore writes 5 to x.
- A9 runs after A8. The only write to x that can follow A8 is B9, which also writes 5. So A9 returns **5**.

**Q2 and Q3: the final values of y and z**

A4 reads y. The writes to y are A1 (5), A2 (4), B5 (6) and A6 (the value A4 read). So A4 returns either 4 or 6.

- **A4 returns 6.** This means B5 took effect between A2 and A4.
  - Nothing writes to y after A6, so the final y is 6.
  - The final z is the later of A5 and B3. A5 writes 6 and B3 writes 6, so the final z is 6.
  - Result: (5, 6, 6).

- **A4 returns 4.** This means B5 took effect before A2 or after A4.
  - The final y is whichever of A6 (4) and B5 (6) takes effect last.
  - The final z is whichever of A5 (4) and B3 (6) takes effect last.
  - All four combinations can happen:
    - y = 4, z = 6: A5 < B3 < B4 < B5 < A6.
    - y = 6, z = 4: B3 < A5 < A6 < B5.
    - y = 4, z = 4: B1–B5 all before A2, then A4, A5, A6.
    - y = 6, z = 6: A6 < B3 < B5.

BEGIN
5 4 4
5 4 6
5 6 4
5 6 6
END