**Possible outcomes (A8, A9, final x, final z):** five combinations, listed at the end.

**1. B2 always returns 0.**
- B2 comes before B4, and B4 is before Q.
- A2 starts after Q, and A writes x only after A2.
- B5 comes after B2.
- So no write to x takes effect before B2, and B9 always writes 0 to y.

**2. A2 returns 6 or 0.**
- A2 starts after both Q and R, so it comes after B1 to B4 have ended. y already holds 6 from B1.
- If B9 has taken effect before A2, then A2 returns 0. Otherwise it returns 6.
- Call the value A2 returns v.

**3. Final z is v.**
- B4 (write 3 to z) is before P.
- A3 (write v to z) is after P, and nothing else writes z.

**4. A8 equals the final value of x.**
- A6 comes before A8 in thread A.
- B5 is before S, and A8 is after S.
- So every write to x has taken effect before A8.
- The final value of x is whichever of A6 (writes v) and B5 (writes 4) takes effect last.

**Case v = 6 (B9 takes effect after A2):**
- B5 can take effect before A6, giving final x = 6, or after it, giving final x = 4.
- A9 can come before B9 and return 6, or after it and return 0.
- These two choices are independent, so this case gives 4 outcomes, all with final z = 6.

**Case v = 0 (B9 takes effect before A2):**
- The order is B5, then B9, then A2, then A6, so A6 is the last write to x. Final x = 0 and A8 = 0.
- A9 comes after B9 and returns 0.
- Final z = 0.

BEGIN
6 6 6 6
6 0 6 6
4 6 4 6
4 0 4 6
0 0 0 0
END