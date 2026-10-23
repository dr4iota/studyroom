Q1 is the value A1 reads from x, Q2 is the value B3 reads from y, and Q3 is the final value of y. Thirteen combinations are possible.

Key facts used:
- C2 must precede A2, since A2 reads y=2 and only C2 or a C5 that writes 2 can supply that value.
- B1 precedes B3 in program order, so b3 is never 0.
- If the final y is 1, B1 comes last among the y-writes, which forces A3 before B2 and makes B5 read b2 = a1. That only works with a1 = 2, so the only outcome with final y = 1 is (2, 1, 1).
- Every other combination with a1 in {0, 2}, b3 in {1, 2, 3}, and final y in {2, 3} has a witness schedule.

BEGIN
0 1 2
0 1 3
0 2 2
0 2 3
0 3 2
0 3 3
2 1 1
2 1 2
2 1 3
2 2 2
2 2 3
2 3 2
2 3 3
END