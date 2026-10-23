Every combination of the three values is possible: 12 in total.

**Q1: value returned by A1 (0 or 4).**
- Only B2 writes y, and it writes 4.
- If A1 takes effect before B2, it returns 0.
- If A1 takes effect after B2, it returns 4. This fits B1 returning 0, because B1 comes before B2.

**Q3: final value of x (2 or 4).**
- A5 is thread A's last write to x, so the final value is decided by A5 (writes 2) and B5 (writes 4).
- Whichever of the two takes effect later sets it, so it is 2 or 4.

**Q2: value returned by B3 (0, 2 or 4).** B3 runs after B2 and before B5, so B5 can never be the write B3 sees.
- **0:** B3 takes effect before A2. Then A2–A5 and B4–B5 can follow in any order, so either final value works.
- **2:** B3 takes effect between A2 and A3. B5 can come before or after A5, so either final value works.
- **4:** B3 takes effect between A3 and A5. B5 can come before or after A5, so either final value works.

**Independence of the choices.**
- A1 only has to come before A2, so it can be placed before or after B2 in each of the cases above.
- If A1 returns 4 (B2 < A1 < A2), B3 can still fall before A2, between A2 and A3, or between A3 and A5.

So 2 × 3 × 2 = 12 combinations are reachable.

BEGIN
0 0 2
0 0 4
0 2 2
0 2 4
0 4 2
0 4 4
4 0 2
4 0 4
4 2 2
4 2 4
4 4 2
4 4 4
END