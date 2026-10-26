Only the write to z by B4 is needed to make B5 return 1, so B4 must take effect before B5. Thread order forces B1 < B2 < B3 in time, and A2 < A3. The possible write orders to y are:

- B3, A2, A3 (values 1, 1, 3): B1 and B2 both read 0.
- A2, B3, A3 (values 1, 1, 3): B1 and B2 read a non-decreasing pair from {0, 1}.
- A2, A3, B3 (values 1, 3, 1): B1 and B2 read a non-decreasing pair from the sequence 0, 1, 3.

That gives (B1, B2) ∈ {(0,0), (0,1), (1,1), (0,3), (1,3), (3,3)}.

A5 is only constrained to come after A4. It can fall before B4 (returns 0) or after B4 (returns 1), and placing it does not restrict the y reads. So A5 ∈ {0, 1} independently, giving 12 combinations.

BEGIN
0 0 0
0 0 1
0 1 1
0 0 3
0 1 3
0 3 3
1 0 0
1 0 1
1 1 1
1 0 3
1 1 3
1 3 3
END