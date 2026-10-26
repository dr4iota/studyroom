The condition that C3 reads 2 forces the write order. The only write of 2 is A2, so C1 < C2 < A2 < C3 in time, and B3 cannot fall between A2 and C3. That leaves four placements for B3:

- **Before C1:** the final value is 2, A1 can be 0, 1, or 3, and B1 must be 0.
- **Between C1 and C2:** the final value is 2, A1 can be 0, 1, or 3, and B1 can be 0 or 1.
- **Between C2 and A2:** the final value is 2, and A1 and B1 can each be 0, 1, or 3 independently.
- **After C3:** the final value is 3, A1 can be 0, 1, or 3, and B1 can be 0, 1, 2, or 3. B1 can be 2 here because it can read after A2 and before B3.

Combining these gives 21 outcomes. Q1 is the value of A1, Q2 is the value of B1, and Q3 is the final value of x.

BEGIN
0 0 2
0 1 2
0 3 2
1 0 2
1 1 2
1 3 2
3 0 2
3 1 2
3 3 2
0 0 3
0 1 3
0 2 3
0 3 3
1 0 3
1 1 3
1 2 3
1 3 3
3 0 3
3 1 3
3 2 3
3 3 3
END