Thread B is the only thread that writes y, and it does so in the order B2 (2), B4 (2), B7 (1). So over time y goes 0, then 2, then 1. Thread A never writes y.

**Reads of y.** A2 comes before A4 in A's program order, so A4 sees a value at the same point or later in that sequence than A2 does. The possible (A2, A4) pairs are (0,0), (0,2), (0,1), (2,2), (2,1) and (1,1). Each is achievable. A3 only needs B1 to have taken effect, so B can run as far as B7 before A2 reads y. Alternatively B can stay behind A2 and A4 entirely.

**Final value of x.**
- B writes only 2 to x (B1 and B3).
- A3 returned 2, so B1 took effect before A3. A1 precedes A3, so A1 read either 0 or 2.
- A5, A6 and A7 each write A1's value to x.
- If A1 read 2, every write to x is 2, so the final x is 2.
- If A1 read 0 (A1 before B1), the final x is 0 when B3 takes effect before A7. Both orders are possible, so the final x is 0 or 2. It is 2 when B3 takes effect after A7.

**Combining.** Final x = 2 is reachable for every (A2, A4) pair by taking A1 = 2. Final x = 0 is reachable for every pair with A1 = 0 and B3 placed before A7.
- For A1 = 0, we need A1 → B1 → … → B7 → A2 in the case A2 = 1. This is possible.
- For A4 = 0, B2 takes effect after A4. B3 then falls between A4 and A7, which is also possible.

So all six y-pairs combine with both final values of x.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 1 0
0 1 2
2 2 0
2 2 2
2 1 0
2 1 2
1 1 0
1 1 2
END