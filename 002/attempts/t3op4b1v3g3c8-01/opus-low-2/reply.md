**Approach.** B3 must read 1, so a write of 1 must take effect before B3 and after B2. The writes of 1 are C4, and A3 if A1 read 1. B2 comes after B1, so B2 never returns 0. It can return 2 (from B1, C1 or C3), 3 (from C2) or 1. The final value of x is the value of whichever of A3, B4 and C4 takes effect last.

**B2 returns 2.**
- **Final 2:** B1, B2 (reads 2), C1, C2, C3, C4, B3 (reads 1), B4 writes 2. A reads 0 and 2 early, and A3 (writes 0) takes effect before C4.
- **Final 0:** B1, B2 (reads 2), C1–C4, B3 (reads 1), B4 writes 2. A1 read 0 at the start, A2 then reads 2, and A3 writes 0 last.
- **Final 3:** A1 reads 3 between C2 and C3, A2 later reads 2, and A3 writes 3 last.
- **Final 1:** B1, B2 (reads 2), C1–C4, A1 (reads 1), B3 (reads 1), B4 (writes 2), A2 (reads 2), A3 writes 1 last.

**B2 returns 3.** B2 takes effect between C2 and C3.
- **Final 3:** B4 writes 3 last.
- **Final 0, 2 or 3:** A3 writes last, with A1 having read 0, 2 or 3. A2 reads 2 from C3.
- **Final 1 is impossible.**
  - If A3 writes 1 last, A1 read 1, so A1 is after C4. A2 then needs a write of 2 after C4. B1 is already before B2 and B4 writes 3, so there is none.
  - If C4 is the last write, B3's 1 must come from A3. That again needs A1 to read 1 before C4, which cannot happen.

**B2 returns 1.**
- **Final 1:** B4 writes 1 last.
- **Final 0, 2 or 3:** A3 writes last, with A1 having read 0, 2 or 3. A2 reads 2 from C3 before C4.
- **Another order with final 1:** C1–C4, A1 (reads 1), B1 (writes 2), A2 (reads 2), A3 (writes 1), B2 (reads 1), B3 (reads 1), B4 (writes 1).

BEGIN
2 0
2 1
2 2
2 3
3 0
3 2
3 3
1 0
1 1
1 2
1 3
END