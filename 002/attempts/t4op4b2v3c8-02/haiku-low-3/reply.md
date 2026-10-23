Every value that can be read or written is 0, 2, or 3, and I found a valid interleaving for each of the 27 combinations of (Q1, Q2, Q3) in {0, 2, 3}³. The problem has no sync points, so I treated any interleaving that respects each thread's program order as valid.

**Key facts:**
- B1 reads y, which only A2 (2) or D2 (3) can change before it, so B1 is 0, 2, or 3. B2 and B4 copy that value.
- C1 reads x, so C1 is 0, 2, or 3. C2 copies it, but C3 always overwrites it afterward, so C2 is never the final x.
- The last x write is A1, C3, B4, or D4. The last y write is A2, B2, or D2.
- A3 can be placed anywhere after A2, so it can read any x value that appears from A2 onward.

**Constructions:**
- **fy = 0:** B1 runs before A2 and D2 (reads 0), and B2 writes 0 last to y. Final x is then set by B4, C3, or D4, and A3 is placed after the matching write. All nine (Q1, Q2) pairs work.
- **fy = 2:** Either A2 is the last y write (with B1 reading 0 or 3), or B2 writes 2 last (with B1 reading 2). Final x can be 0, 2, or 3 by choosing B4, C3, or D4 as the last x write, and A3 can read any value in between. All nine pairs work.
- **fy = 3:** D2 is the last y write (with B1 reading 0 or 2), or B2 writes 3 last. Final x and A3 can again be chosen independently. All nine pairs work.

Q1 is the value A3 returns, Q2 is the final x, and Q3 is the final y.

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