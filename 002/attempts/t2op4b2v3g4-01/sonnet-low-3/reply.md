With no sync points, the only ordering constraints are each thread's own program order.

**Constraints**
- B1 returned 0, so no write to x took effect before it. A4 therefore comes after B1. B2 comes after B1 anyway.
- A4 comes after A2 and A3, so neither read can see A4's write. They see only B's writes.
- The values of x that B's writes produce, in order, are 0, 3, 2, 1.
- A2 and A3 are in program order, so A3 sees the same state as A2 or a later one.

**Possible (A2, A3) pairs**
(0,0), (0,3), (0,2), (0,1), (3,3), (3,2), (3,1), (2,2), (2,1), (1,1).

**Final value of x**
- The final value is 2 if A4 takes effect after B4. This is always possible, since A4 can be delayed.
- The final value is 1 if A4 takes effect before B4. This requires A3 to have read a state before B4's write, so A3 ≠ 1.
- If A3 = 1, B4 has already taken effect, so A4 comes after it and the final value is 2.

BEGIN
0 0 1
0 0 2
0 3 1
0 3 2
0 2 1
0 2 2
0 1 2
3 3 1
3 3 2
3 2 1
3 2 2
3 1 2
2 2 1
2 2 2
2 1 2
1 1 2
END