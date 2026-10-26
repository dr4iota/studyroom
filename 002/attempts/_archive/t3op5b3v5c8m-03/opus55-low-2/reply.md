All 12 combinations of (B1, final x, final z) are possible. There are no sync points, so every interleaving that keeps each thread's own order is allowed.

**Possible values**
- **B1** reads x, which holds either 0 or A1's 2. B4's write cannot come before B1, because B4 comes after B1 in thread B. So B1 is 0 or 2.
- **B2** reads y before B3 runs, so it sees 0 or the value written by C3 or C4, which is C2's value.
- **C2** reads x, which can hold 0, 2, or B4's value. B4 writes B2's value, so C2 could only read B4's write if B2 came before B4, B4 before C2, and C2 before C3. Then B2 runs before any write to y and returns 0. So C2 is 0 or 2, and B2 is 0 or 2.
- **Final x** is 2 if B4 takes effect before A1. Otherwise it is B2's value, so it is 0 or 2.
- **Final z** is 3 if C1 is the last write to z. Otherwise it is A3's value, and every write to y is 0 or 2. So z is 0, 2 or 3.

**Each case can actually happen**
- **B1 = 0, x = 0, z = 2:** B1, A1, B2, C1, C2 (reads 2), C3, A2, A3 (reads 2), A4, B3, B4 (writes 0).
- **B1 = 0, x = 0, z = 0:** B1, A1, B2, C1, A2, A3, A4, then C2, C3, C4, B3, B4.
- **B1 = 0, x = 0, z = 3:** A4 takes effect before C1, then C1 writes 3.
- **B1 = 0, x = 2:** all of thread B runs before A1, so A1's 2 is final. z can be 0, 2 or 3 as above; for z = 2, C2 reads x after A1.
- **B1 = 2, x = 0:** B1 runs after A1, and B2 reads 0 before C3. For z = 2, A3 reads B3's 2.
- **B1 = 2, x = 2:** C2 reads 2 and C3 runs before B2, so B2 reads 2 and B4 writes 2. z can again be 0, 2 or 3.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
END