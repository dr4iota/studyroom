**Fixed facts**
- **B2 returns 0.** B2 is above B4 in thread B, so it happens before P. Every write to x by thread A (A4, A5, A6) comes after P, and B5 is after B2 in thread B. So no write to x takes effect before B2. As a result, B9 writes 0 to y.
- **A2 returns 6 or 0.** A2 is after Q and R, so it comes after B1 (which wrote 6 to y). Call A2's value v. If no B8 or B9 write comes between B1 and A2, then v = 6 (B8 also writes 6). If A2 comes after B9, then v = 0.
- **A8 always equals the final x.** A8 is after S, B5 is before S, and A6 comes before A8 in thread A. So every write to x takes effect before A8.
- **Final z is v.** A3 writes v to z after P. B4, the only other write to z, comes before P.

**Case v = 0 (A2 after B9).**
- B9 comes after B5, so A6 (which follows A2) comes after B5. Final x = 0.
- A9 comes after B9, so A9 returns 0.
- Result: 0 0 0 0.

**Case v = 6 (A2 before B9).**
- Final x can be 6: B5 takes effect before A6.
- Final x can be 4: A6 takes effect before B5, with B5 still before S.
- A9 can be 6 (B9 after A9) or 0 (B9 before A9).
- None of these choices restrict each other, so all four combinations are possible.

BEGIN
0 0 0 0
6 6 6 6
6 0 6 6
4 6 4 6
4 0 4 6
END