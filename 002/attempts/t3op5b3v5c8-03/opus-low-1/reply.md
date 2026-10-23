**Key observation:** z is written only by A5, and A5 comes after A3. So A3 must read 0. A4 therefore writes 0 to y.

**Writes to y:**
- A1 writes 3.
- A4 writes 0, and always comes after A1.
- C1 writes 2.
- B2 writes 5, between B1 and B4.

**Possible values:**
- **B1** happens before B2, so it can see 0 (initial value or A4), 3, or 2.
- **B4** happens after B2, so it can see 5, or any write that lands between B2 and B4: 0, 2, or 3.
- **Final y** is set by whichever of A4, C1 or B2 takes effect last, giving 0, 2 or 5. A1 cannot be last because A4 follows it.

**Case analysis on the last write:**

- **Final y = 5 (B2 last):** B4 must read 5. B1 can read 0, 3 or 2.

- **Final y = 2 (C1 last):** B1 cannot read 2, because C1 would then come before B2 and not be last.
  - B4 = 5: B1 is 0 or 3.
  - B4 = 2 (C1 between B2 and B4): B1 is 0 or 3.
  - B4 = 0 (A4 between B2 and B4): B1 is 0 or 3.
  - B4 = 3: A1 must come after B2, so B1 can only be 0.

- **Final y = 0 (A4 last):**
  - B4 = 5: B1 can be 0, 3 or 2.
  - B4 = 2 (C1 after B2): B1 is 0 or 3.
  - B4 = 3 (A1 after B2): B1 is 0 or 2.
  - B4 = 0 (A4 before B4): B1 can be 0, 3 or 2.

BEGIN
0 5 5
3 5 5
2 5 5
0 5 2
3 5 2
0 2 2
3 2 2
0 0 2
3 0 2
0 3 2
0 5 0
3 5 0
2 5 0
0 2 0
3 2 0
0 3 0
2 3 0
0 0 0
3 0 0
2 0 0
END