**Constraints**

- **A3 returns 4.** The only write of 4 to y is B1, so B1 takes effect before A3.
- **A1 (read y).**
  - If A1 takes effect before B1, it returns 0.
  - If A1 takes effect after B1, it returns 4.
  - Both are allowed, because B1 only has to come before A3.
- **B2 and B3 (read z).**
  - z is written by A2 (3), then A4 (4), then B5 (1).
  - B5 comes after B3 in thread B, so neither B2 nor B3 can ever see 1.
  - B2 comes before B3, so their reads follow z's history in order: 0, then 3, then 4. B3 can never return an earlier value than B2.
  - The possible (B2, B3) pairs are therefore (0,0), (0,3), (0,4), (3,3), (3,4) and (4,4).

**Independence of A1 from the z reads**

- **A1 = 0:** A1 takes effect before B1, which is before B2 and B3. The z reads are not otherwise restricted, so all six pairs work.
- **A1 = 4:** order the effects as B1, then B2, then A1, then A2, and so on. B2 and B3 can still fall anywhere relative to A2 and A4, so all six pairs work. For example, B2 can read 0 by taking effect before A2.

That gives 2 × 6 = 12 combinations.

Values in the order Q1 (A1), Q2 (B2), Q3 (B3):

BEGIN
0 0 0
0 0 3
0 0 4
0 3 3
0 3 4
0 4 4
4 0 0
4 0 3
4 0 4
4 3 3
4 3 4
4 4 4
END