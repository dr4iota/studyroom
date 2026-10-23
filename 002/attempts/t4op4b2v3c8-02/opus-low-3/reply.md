All 27 combinations are possible: each asked value can be 0, 2 or 3, independently of the others. There are no sync points, so any interleaving that keeps each thread's order is allowed. Below, b is the value B1 reads from y and c is the value C1 reads from x.

**Which values each quantity can take**
- **b:** B1 runs before B2, so B1 reads 0 (if it runs before A2 and D2), 2 or 3.
- **Final y:** the last write to y is A2 (2), D2 (3) or B2 (b). So final y can be 0, 2 or 3.
- **Final x:** the last write to x is A1 (2), C3 (2), D4 (3) or B4 (b). C2 can never be last because C3 follows it. So final x can be 0, 2 or 3. It is 0 only when b = 0 and B4 is last.
- **A3:** A3 returns the latest write to x before it. That can be 2 (A1, C3, D1), 3 (D3, D4), b (B4) or c (C2). A3 returns 0 if B4 comes just before A3 with b = 0, or if C1 reads 0 before A1 and C2 runs after A1 but before A3.

**Showing the combinations work together**
- **Final y = 0:** run B1 before A2 and D2, and B2 after both. Then b = 0, and B4 comes after A1 and D1.
  - Final x = 0: put B4 last.
  - Final x = 2: put C3 last.
  - Final x = 3: put D4 last.
  - A3 can be placed to read 0 (just after B4), 2, or 3 (just after D3 or D4) before that final write.
  - Example for (0, 0, 0): A1, A2, D1, D2, D3, D4, C1, C2, C3 run first (B1 goes before A2), then B2, B3, B4, A3.
- **Final y = 2:** let B1 read 0 early, then run B2 and D2 before A2 so A2 is the last write to y. Thread B and the writes to x are still free enough to give each of the 9 (A3, final x) pairs, as in the y = 0 case.
- **Final y = 3:** let B1 read 0 early, with A2 before D2 and D2 as the last write to y. A3 can run between A2 and D2 or after B4. Final x can again be 0 (B4 last, after D4), 2 or 3, so all 9 pairs work.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 2
0 3 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
2 3 0
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 2 0
3 2 2
3 2 3
3 3 0
3 3 2
3 3 3
END