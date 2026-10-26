The only possible final value of y is **1**, because x = 4 at the end forces the last write to y to be A3.

**Writes to y.** Only A3 (writes 1) and B2 (writes 4) touch y. So the final y is 1 or 4, depending on which of these takes effect last.

**Which write leaves x = 4.** The writes to x are A1 (1), A2 (4), B3 (5), B4 (2) and C4 (the value C1 read). The last of these must write 4, so it is either A2 or C4 with C1 having returned 4.

**C1 cannot have returned 4.**
- The only write that could put 4 into z is A5. It does so only if A4 read 4, which needs B2 to come after A3 and before A4.
- B1 (z = 3) comes before B2 in thread B, so B1 is already done before A5 writes 4.
- If C1 returned 4, then A5 came before C1, and C2 comes after C1.
- C2 must return 3, but the only 3 written to z after A5 would be C3's, and C3 comes after C2.
- So C2 could not return 3, which contradicts the known result. Therefore C1 did not return 4, and C4 cannot be the write that leaves x = 4.

**A2 is the last write to x.** Then B3 and B4 take effect before A2. In thread B, B2 comes before B3, so B2 is before A2. In thread A, A2 comes before A3. So B2 takes effect before A3, and A3 is the last write to y. The final y is therefore 1.

**A valid execution exists.** Run B1, B2, B3, B4, then C1 (returns 3), C2 (returns 3), C3, C4 (writes 3 to x), C5, and finally A1 through A5. A2 is the last write to x, so x = 4 at the end, and y = 1.

BEGIN
1
END