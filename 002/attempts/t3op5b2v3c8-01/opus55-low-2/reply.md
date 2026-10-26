All 27 combinations are possible: each of Q1, Q2 and Q3 can be 0, 3 or 2, in any mix. This was worked out by hand, not checked with a tool.

**Possible values**
- y only ever holds 0, 3 or 2. C4 copies a value C3 read from y, so it adds nothing new.
- x only ever holds 0, 3 or 2. B5 copies a y value, and C2 copies an x value.
- So each asked read returns 0, 3 or 2.

**Why x can move between any two values**
A2 must come before A3 in time, so every ordered pair of x values has to be reachable.
- **0 → 3:** B1 writes 3.
- **0 → 2:** B4 reads 2 after B3, then B5 writes 2.
- **3 → 0:** C1 reads 0 before B1, and C2 runs after B1.
- **3 → 2:** B5 writes 2.
- **2 → 0:** C1 reads 0 before B1, and C2 runs after B5 wrote 2.
- **2 → 3:** C1 reads 3 between B1 and B5, and C2 runs after B5.
- **Same value twice:** A2 and A3 run with no write to x between them.

**Checking each value of A1**
- **A1 = 0:** A1 runs before B2 and C4. Every x pattern above can still happen afterwards, so all 9 pairs work.
- **A1 = 3:** A1 runs after B2. Each x pair can still be built afterwards. The hardest is (0, 3), which works with this order: B1, B2, A1, C2 (writes 0, since C1 read 0 earlier), C3 (reads 3), B3, C4 (writes 3), A2 = 0, B4 (reads 3), B5 (writes 3 to x), A3 = 3.
- **A1 = 2:** A1 runs after B3. The hardest case is again (0, 3). It works with this order: C1 (reads 0), B1, B2, C2 (writes 0), C3 (reads 3), B3, A1 = 2, A2 = 0, C4 (writes 3), B4 (reads 3), B5 (writes 3 to x), A3 = 3.

BEGIN
0 0 0
0 0 3
0 0 2
0 3 0
0 3 3
0 3 2
0 2 0
0 2 3
0 2 2
3 0 0
3 0 3
3 0 2
3 3 0
3 3 3
3 3 2
3 2 0
3 2 3
3 2 2
2 0 0
2 0 3
2 0 2
2 3 0
2 3 3
2 3 2
2 2 0
2 2 3
2 2 2
END