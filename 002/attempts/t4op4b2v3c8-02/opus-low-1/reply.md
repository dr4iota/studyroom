All 27 combinations of (A3, final x, final y) are possible, with each value in {0, 2, 3}.

**Possible values for each quantity**
- **Writes to x:** A1, C3 and D1 write 2. D3 and D4 write 3. B4 writes whatever B1 read from y, which is 0, 2 or 3. C2 writes whatever C1 read from x, which is 0, 2 or 3. So every value of x is in {0, 2, 3}.
- **Writes to y:** A2 writes 2, D2 writes 3, and B2 writes B1's value (0, 2 or 3). So every value of y is in {0, 2, 3}.
- **Final y = 0** happens when B1 runs before A2 and D2 and so reads 0, and B2 runs after both of them.
- **Final x = 0** happens when B1 read 0 and B4 is the last write to x. C2 can never be the last write to x, because C3 always follows it.

**A3 = 0**
- A3 must read a 0 written by C2 (with C1 run before any write to x, so it read 0) or by B4 (with B1 having read 0).
- **Final x = 2 or 3:** C1 runs first and reads 0. C2 writes 0 after A1 and immediately before A3, with every write by D placed either before C2 or after A3. Then C3 or D4 can be the last write to x.
- **Final x = 0:** B4 (writing B1's 0) can be the last write to x.
- **Final y:** y depends only on the order of B1, B2, A2 and D2. B1 can run before A2 and D2 in every case above, so final y can be made 0, 2 or 3 independently.

**A3 = 2**
- A3 runs right after A1, before any other write to x.
- The writes to x and y that happen afterwards can still be ordered to give any final x and final y.

**A3 = 3**
- A3 runs right after D3.
- Later writes can still make final x equal 0, 2 or 3, for example B4 last with B1 having read 0.
- Final y is again free.

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