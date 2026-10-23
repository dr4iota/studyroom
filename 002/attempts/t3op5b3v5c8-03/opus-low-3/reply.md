The listed combinations are all the possible (B1, B4, final y) triples.

**Step 1: A3 always returns 0.**
Only A5 writes to z, and A5 comes after A3 in thread A. So no write to z takes effect before A3, and A3 returns 0. As a result, A4 writes 0 to y and A5 writes 0 to z.

**Step 2: The writes to y.**
- A1 writes 3.
- A4 writes 0, and A4 takes effect after A1.
- B2 writes 5.
- C1 writes 2.

Within thread B, B1 takes effect before B2, and B2 before B4. The final value of y comes from whichever of A4, B2 or C1 takes effect last. A1 can never be last because A4 follows it. So the final y is 0, 5 or 2.

**Case 1: final y = 5 (B2 is the last write to y).**
- No write to y follows B2, so B4 returns 5.
- B1 can return 0 (initial value or A4's 0), 2 (after C1) or 3 (after A1).
- Combinations: (0,5,5), (2,5,5), (3,5,5).

**Case 2: final y = 0 (A4 is the last write to y).**
- **B4 = 0:** B4 takes effect after A4. B1 can return 0, 2 or 3.
- **B4 = 5:** B4 takes effect after B2 but before A4, and C1 is not between B2 and B4. B1 can return 0, 2 or 3.
- **B4 = 3:** A1 takes effect between B2 and B4. B1 comes before B2, so it is also before A1 and cannot see 3. It can return 0 (initial) or 2 (after C1).
- **B4 = 2:** C1 takes effect between B2 and B4. B1 comes before C1, so it cannot see 2. It can return 0 or 3.

**Case 3: final y = 2 (C1 is the last write to y, so C1 takes effect after B2).**
B1 takes effect before B2, so it comes before C1 and can never return 2.
- **B4 = 2:** B4 takes effect after C1. B1 can return 0 or 3.
- **B4 = 5:** no write to y between B2 and B4. B1 can return 0 or 3.
- **B4 = 3:** A1 takes effect between B2 and B4, so B1 comes before A1. A4 follows A1, so B1 returns 0 (initial value).
- **B4 = 0:** A4 takes effect between B2 and B4. B1 can return 0 or 3. For example, the order A1, B1, B2, A4, B4, C1 gives B1 = 3.

BEGIN
0 5 5
2 5 5
3 5 5
0 0 0
2 0 0
3 0 0
0 5 0
2 5 0
3 5 0
0 3 0
2 3 0
0 2 0
3 2 0
0 2 2
3 2 2
0 5 2
3 5 2
0 3 2
0 0 2
3 0 2
END