Every combination is listed below. The reasoning follows.

**Timing constraints.** B1–B7 all end before P. A2 starts before P and ends after P, and it ends before Q. C5 ends after Q, and C6 ends before R. A5 and A6 come after R. So A3 and A4 come after P, while C2, C3 and C5 can take effect before P.

**Values written to y before P.** These come from B1 (3), B5 (2), C2 (the value C1 read, 0 or 1), C3 (3) and C5 (3). Since C2 < C3 < C4 < C5 in thread order, C4 reading 3 means no write other than a 3 lands between C3 and C4.

**Q1 and Q2 (B6, B7).** B6 and B7 come after B5 (value 2). They can be overwritten only by C2, C3 or C5, in that order. C2 writes v, the value C1 read, which is 0 or 1. The possible (B6, B7) pairs are:
- (2,2), (2,v), (2,3)
- (v,v), (v,3)
- (3,3)

**Q3 (final y).**
- A4 writes 3 and A5 writes A1's value, which is 0 or 1. C6 is before R, so it cannot be last. The final value of y is therefore 3 or A1's value, so it is 0, 1 or 3.
- C7 returns 0, so the last write to y before C7 must be a 0. That write is either C6 with C1 = 0, or A5 with A1 = 0.
- If A1 = 1, then A5 cannot supply that 0, so C1 must be 0, which makes v = 0. So when v = 1, A1 must be 0, and the final y is 0 (A5 last) or 3 (A4 last). The final y cannot be 1.
- When v = 0, A1 = 1 is possible, so all of 0, 1 and 3 are allowed.
- A2 reading 3 is satisfiable in all cases, for example by reading right after B1.

BEGIN
2 2 0
2 2 1
2 2 3
2 0 0
2 0 1
2 0 3
2 3 0
2 3 1
2 3 3
0 0 0
0 0 1
0 0 3
0 3 0
0 3 1
0 3 3
3 3 0
3 3 1
3 3 3
2 1 0
2 1 3
1 1 0
1 1 3
1 3 0
1 3 3
END