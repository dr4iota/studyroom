Block x is never written, so B2 always returns 0 and adds no constraint. There are no sync points, so any interleaving that keeps each thread's order is allowed.

**Possible values of each read**
- **A2** comes after A1 and before A3. It returns 3 from A1, unless B4 or B5 takes effect between A1 and A2. So A2 can return 3, 1 or 2.
- **B3** comes before B4, so it can only see A's writes or the initial value. It can return 0 (before A1), 3 (after A1) or 4 (between A3 and A4).
- **Final y** is set by whichever of A4 (writes 3) and B5 (writes 2) takes effect last. So it is 3 or 2.

**Case A2 = 1:** B4 takes effect between A1 and A2, and B5 after A2.
- B3 comes before B4, so it is before A3. It returns 0 if it is before A1, or 3 if it is after A1.
- B5 can be before or after A4, so the final y is 3 or 2.
- This gives 4 combinations.

**Case A2 = 2:** both B4 and B5 take effect between A1 and A2.
- B3 returns 0 or 3, as in the previous case.
- A4 comes after B5, so the final y is 3.
- This gives 2 combinations.

**Case A2 = 3:** no B write falls between A1 and A2.
- **B3 = 0:** B3 is before A1. B4 and B5 can run either before A1 (final 3) or after A4 (final 2).
- **B3 = 3:** B3 is after A1. If B5 is between A2 and A3, the final y is 3. If B5 is after A4, it is 2.
- **B3 = 4:** B3 is between A3 and A4. If B4 and B5 are before A4, the final y is 3. Otherwise it is 2.
- This gives 6 combinations.

BEGIN
1 0 3
1 0 2
1 3 3
1 3 2
2 0 3
2 3 3
3 0 3
3 0 2
3 3 3
3 3 2
3 4 3
3 4 2
END