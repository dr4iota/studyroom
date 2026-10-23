The approach is to enumerate interleavings by cases on the value read by A1. There are no sync points, so any interleaving that keeps each thread's program order is allowed.

**Background facts**
- z is written by B1 (1), C1 (2), and by A2 and A3, which write a, the value read by A1.
- x is written only by C2 (1). So B2 reads 0 or 1; call that value b. B3 then writes b to y.
- The final y is whichever of A4 (writes a) and B3 (writes b) takes effect last.

**Case a = 0 (A1 reads z before B1 and C1)**
- C4 and B5 can each return 0, 1 or 2, except the pair (B5 = 2, C4 = 1).
  - C4 = 1 needs B1 after C1. Then B5 comes after B1 and can only see 1 or a later 0.
- The final y can be 0 or 1 for every allowed pair, with one exception: (B5 = 2, C4 = 0, y = 1) is impossible.
  - B5 = 2 forbids any A write between C1 and B5.
  - C4 = 0 needs an A write after C1. So A3 lands after B5, and A4 after that.
  - B3 comes before B5, so A4 is last and y = 0, not 1.

**Case a = 1 (A1 reads B1's write)**
- B5 and C4 can each be 1 or 2; every pair is possible.
- The final y can be 1 for every pair.
- The final y can be 0 (B2 reads 0, B3 last) except for (B5 = 2, C4 = 1).
  - C4 = 1 needs an A write after C1. B5 = 2 needs C1 to be the last write before B5.
  - So A3 comes after B5, which is after B3. A4 is then last and y = 1.
  - Example for (2, 1, 1): B1, A1, C1, B2–B5, A2, A3, A4, C2, C3, C4.

**Case a = 2 (A1 reads C1's write)**
- B5 and C4 can each be 1 or 2; every pair is possible.
- The final y can be 0, 1 or 2 for every pair.
  - Example for (2, 1, 0): C1, A1, B1, B2 (reads 0), C2, C3, C4 (reads 1), A2, A3, A4, B3, B4, B5 (reads 2).

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 0 0
1 0 1
1 1 0
1 1 1
1 1 2
1 2 0
1 2 1
1 2 2
2 0 0
2 2 0
2 2 1
2 2 2
2 1 0
2 1 1
2 1 2
END