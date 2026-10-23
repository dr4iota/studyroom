**C3 always returns 0. The final z can be 0, 1 or 5.** Rule 6 does not come into play because the problem has no sync points. So every execution is just some interleaving of the operations, kept in each thread's order.

**Q1: value returned by C3**

1. The only write to z is B5.
2. If B5 takes effect after C3, then C3 reads the initial value, 0.
3. If B5 takes effect before C3, it is also before C4, because C3 comes before C4 in thread C. C4 is known to return 0, so B5 must have written 0. Then C3 also reads 0.
4. So **C3 always returns 0**.

**Q2: final value of z**

The final z is whatever B5 writes, which is the value B4 read from y.

1. B4 comes after B3 (which writes 1 to y), so B4 reads the last write to y at or after B3.
2. The writes to y are:
   - B1 writes 2, but it is before B3, so B4 can never see it.
   - B3 writes 1.
   - C1 writes 1.
   - A4 writes whatever A1 read from x, which is 0 or 5.
3. So B4 can read 1, 0 or 5.

Each case has a valid order:

- **z = 1:** B1, B2, C1–C5, A1–A5, B3, B4, B5.
  - A3 reads 5 because B2 came first.
  - A2 and C4 read 0 because they are before B5.
- **z = 0:** B1, A1 (reads 0), A2, B2, A3, B3, A4 (writes 0), B4, B5, then C1–C5.
  - B5 writes 0, so C4 still reads 0.
- **z = 5:** B1, B2, C1–C5, A1 (reads 5), A2, A3, B3, A4 (writes 5), B4, B5, A5.
  - A2 and C4 are before B5, so both read 0.

BEGIN
0 0
0 1
0 5
END