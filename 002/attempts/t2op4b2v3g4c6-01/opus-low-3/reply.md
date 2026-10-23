Every combination below is possible, and nothing else is.

**Constraints that matter**

- No sync points are used, so the only ordering limits are each thread's program order and the known read results.
- B1 returns 0, and nothing else in thread B writes x before it.
- A1 returns 0, which always holds because nothing writes y.
- The writes to x by thread B take effect in the order 3, 2, 1 (B2, B3, B4).
- A4 comes after A3, so A2 and A3 can only see the initial 0 or one of B's writes.

**Q1 and Q2 (A2 and A3)**

A2 takes effect before A3. So A3 sees the same value as A2 or a later one in the sequence 0 → 3 → 2 → 1. That gives 10 pairs:
(0,0), (0,3), (0,2), (0,1), (3,3), (3,2), (3,1), (2,2), (2,1), (1,1).

**Q3 (final x)**

A4 writes the value A3 read. The final value of x comes from whichever of A4 or B4 takes effect last.

- If A3 read 1, B4 took effect before A3, so A4 comes after B4. The final value is 1.
- If A3 read 0, 3 or 2, both orders of A4 and B4 are possible. The final value is either 1 or A3's value.
- When A3 read 0, A4 writes 0. That does not conflict with B1 returning 0, whenever A4 takes effect.

BEGIN
0 0 0
0 0 1
0 3 3
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END