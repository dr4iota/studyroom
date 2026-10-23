Every combination of the three asked values is possible, 27 in total.

No sync points are given, so the operations of the four threads can interleave in any order, each thread keeping its own order.

**Values that can be read**
- B1 reads y, which can be 0, 2 or 3. Call that value b1.
- B2 and B4 write b1. C1 reads x, and C2 writes that value back to x.

**Q3 (final y)** is the last write among A2 (2), B2 (b1) and D2 (3).
- y = 2 when A2 is last.
- y = 3 when D2 is last.
- y = 0 when B1 reads 0 before A2 and D2, and B2 is delayed until after both.

**Q2 (final x)** is the last write among A1, B4, C3, D1, D3 and D4.
- x = 2 when C3 is last.
- x = 3 when D4 is last.
- x = 0 when B1 read 0 and B4 (which writes 0) is the last write to x.
- C2 always comes before C3, so it can never be the last write.

**Q1 (A3)** reads x after A1, so it sees the last write to x before it.
- A3 = 2 after A1 alone.
- A3 = 3 after D3.
- A3 = 0 when C1 read 0 before A1 and C2 then writes 0 before A3, or when B4 writes 0 before A3.

**Independence of the three values**
- The writes that fix A3 can be placed early, before the writes that fix the final x and y.
- A late B2, B4, C3 or D4 can then supply the final values without changing what A3 saw.
- Choosing y = 0 forces b1 = 0, so B4 writes 0 to x. That is harmless, because C3 or D4 can overwrite it afterwards.
- Choosing x = 0 also forces b1 = 0, but B2 only needs to run after B1. A2 or D2 can still be last, so y can be 0, 2 or 3.

So A3, final x and final y can each independently be 0, 2 or 3.

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