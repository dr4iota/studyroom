Every combination of an allowed (A2, A4) pair with a final x of 0 or 2 is possible, giving 12 outcomes.

**Values available for A1 and A3**
- Thread A never writes to y. Thread B writes 2 to y (B2, B4) and then 1 to y (B7). So any read of y returns 0, 2 or 1.
- A3 returned 2, so A3 takes effect after B1.
- A1 returns 0 if it takes effect before B1, and 2 otherwise.

**Q1 and Q2 (A2 and A4)**
- A2 takes effect before A4, and the values of y over time are 0, then 2, then 1.
- So the A4 value can never be earlier in that sequence than the A2 value.
- A2 = 0 is possible with A4 = 0, 2 or 1.
- A2 = 2 is possible with A4 = 2 or 1.
- A2 = 1 forces A4 = 1.

**Q3 (final x)**
- The last write to x is either A7 (which writes the A1 value) or B3 (which writes 2).
- If A1 returned 2, the final x is 2 either way.
- If A1 returned 0, the final x is 0 when A7 takes effect after B3, and 2 when B3 takes effect after A7.

**Each (A2, A4) pair with each final x**
- **Final x = 0:** A1 takes effect before B1, A3 after B1, and A5–A7 after B3. The reads of y can still be placed anywhere relative to B2, B4 and B7.
  - For A4 = 0, A4 must come before B2. Then the order A1, B1, A3, A2, A4, B2, B3, A5, A6, A7 works.
  - For A2 = 1, A2 comes after B7. B3 is then already done, so A3 reads 2 and A7 lands after B3.
- **Final x = 2:** Use A1 = 2, or A1 = 0 with B3 after A7. Neither choice interferes with the reads of y.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 1 0
0 1 2
2 2 0
2 2 2
2 1 0
2 1 2
1 1 0
1 1 2
END