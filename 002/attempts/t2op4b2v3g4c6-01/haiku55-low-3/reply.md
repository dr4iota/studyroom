Thread order is fixed, and B's writes to x take effect in the order 3, 2, 1. A4 writes whatever A3 read, and it may land anywhere after A3.

- **A2 and A3:** Neither read can see A4, because A4 comes after A3. So they see a non-decreasing prefix of B's writes, giving 10 possible (A2, A3) pairs.
- **Final x:** If A4 takes effect after B4, the final value is A3's value. If A4 takes effect before B4, the final value is 1. A4 can take effect before B4 only when A3 reads before B4, so the final value is 1 in that case.
- **Constraint from B1:** B1 must read 0, which is achievable by placing B1 before any nonzero write.

Combining these gives 16 outcomes.

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