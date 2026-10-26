Every execution gives a final y of 3, and the final z equals whatever C4 returns, so the only open question is which values C4 can return.

**Constraints from the known results**

- The only write to y is B2, which writes 3. A3 returned 3, so B2 takes effect before A3. A2 comes before A3, so A2 returns 0 or 3. The final y is therefore always 3.
- The writes to x are A1 (2), A4 (A2's value, which is 0 or 3) and B5 (1).
- B1 returned 0 and runs before B2. A4 comes after A3, which is after B2, which is after B1. So B1 takes effect before A4, and the only way B1 can see 0 is for it to take effect before A1. This gives B1 < A1.
- The writes to z are C1 (4), B3 (3), C3 (2) and C5. C2 returned 3, so C1 < B3 < C2, and C3 and C5 come after C2. C5 is therefore the last write to z, and the final z equals C4's value.

**Values C4 can return**

- 0: the order B1, B2, B3, C2, C3, C4, then A1 works, because C4 reads x before any write to it. A2 then reads 3, and the later reads still fit.
- 2: C4 reads x after A1 and before A4 and B5 take effect.
- 1: B5 takes effect, then C4 reads. A4 either comes earlier or is still later.
- 3: A2 reads 3 and A4 writes 3. C4 reads x after A4 and either before B5 or after B5 has been overwritten by A4.

Each of these cases is consistent with all the known results.

BEGIN
0 3 0
1 3 1
2 3 2
3 3 3
END