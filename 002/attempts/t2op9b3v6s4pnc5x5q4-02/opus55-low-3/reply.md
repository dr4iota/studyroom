**Ordering constraints from the sync points**

- A1, A2 and A3 happen before Q. B2, B3 and B4 happen after Q.
- B1 through B4 happen before R. A4 through A8 happen after R.
- B1 through B6 happen before P. A9 happens after P.
- A1 happens before S, and B3 happens after S.

**Fixed values**

- **A3 reads z.** The only writes to z that can come before A3 are A1's. B4 is after Q, so A3 returns 1.
- **A4 to A6.** B4 comes before R, so B4 is already done. A4, A5 and A6 then write 1, 6 and 1 to z.
- **A9** writes A3's value, so it writes 1 to x.

**Q1: A7 reads z**

- The only write to z that can still land between A6 and A7 is B8, which writes 3.
- So A7 returns 1 or 3.
- A7 = 3 needs B8 to take effect between A6 and A7.

**Q2: B6 reads x**

- B6 comes after B3, which wrote 3.
- If A8 takes effect between B3 and B6, B6 returns A7's value instead.
- In that case A7 is before B6, and B8 comes after B6. So A7 must have read 1, and B6 returns 1.
- Otherwise B6 returns 3.

**Q3 and Q4: final x and z**

- Final x is set by whichever of A9 (writes 1) and B7 (writes 5) is last.
- B7 can be last only if B8, which follows B7, also comes after A7. That forces A7 = 1 and final z = 3.
- Final z is set by whichever of A6 (writes 1) and B8 (writes 3) is last.
- If A6 is last (z = 1), then B8 came before A6. That gives A7 = 1, B6 = 3 and final x = 1.

**Cases**

- **A7 = 3:** B8 is between A6 and A7, so B8 is before A9 and B7 is before B8. B6 = 3, x = 1, z = 3.
- **A7 = 1, B6 = 3:** three outcomes are possible: (x, z) = (1, 1), (1, 3) or (5, 3).
- **A7 = 1, B6 = 1:** B8 comes after B6, which is after A7, so z = 3. Final x can be 1 or 5.

BEGIN
3 3 1 3
1 3 1 1
1 3 1 3
1 3 5 3
1 1 1 3
1 1 5 3
END