A6 always returns 1. The final value of z can be 3 or 5.

**1. B3 must have read 3.** The writes to z are A1 (2), A2 (5), C6 (1) and B8 (the value B3 read). C8 returned 3, so the last write to z before C8 must be B8, and B3 must have read 3. B8 also takes effect after C6 and before C8.

**2. B4 sits between A1 and A2.** B4 returned 2, so A1 takes effect before B4. Neither A2 nor C6 can fall between them. Since A2 comes after A1 in thread A, A2 must come after B4.

**3. Q1: A6 returns 1.** A3 returned 2 from y. The only writes to y are C2 (5), C3 (2), A4 (1) and A8. So C3, and therefore C2, takes effect before A3. A4 then writes 1, and A8 comes after A6. So no other write to y can land between A4 and A6, and A6 returns 1.

**4. Q2: the final value of z is 3 or 5.** The last write to z is either B8 (3) or A2 (5). C6 must come before B8, so z cannot end at 1.

- **z = 3:** A2 takes effect before C6, so B8 is the last write to z.
- **z = 5:** this order satisfies every rule:
  - A1, then B1, B2, B3 (all reading x = 3), then B4 (reads z = 2).
  - C1 to C6, then B5 to B8 (z becomes 3), then C7, then C8 (reads 3).
  - A2 (z becomes 5), then A3 (reads y = 2, since C3 is done) through A8.
  - A7 reads x = 3, and the last write to x is C7 (3), so x ends at 3 as required.

BEGIN
1 3
1 5
END