Four writes to x matter: C1 (1), C2 (3), A2 (2), B3 (3).

**Constraints from C3 returning 2.** The only write of 2 is A2, so A2 must be the last write to x before C3. This gives C1 < C2 < A2 < C3, and B3 must not fall between A2 and C3. A1 must come before A2, and B1 < B2 < B3.

**Q1 (A1).** A1 reads before A2, so it can never see 2. It can see 0, 1 or 3.

**Case 1: B3 is before A2, so the final x is 2.**
- B1 is before B3, so it cannot see 2. It can see 0, 1 or 3.
- B1 = 3 needs the order C1, C2, B3, with B1 after C2. A1 can still read 0, 1 or 3 in each order.
- So A1 ∈ {0, 1, 3} and B1 ∈ {0, 1, 3} can be combined freely, giving 9 combinations.

**Case 2: B3 is after C3, so the final x is 3.**
- The order is C1 < C2 < A2 < C3 < B3.
- B1 can be anywhere before B3, so it can see 0, 1, 3 or 2.
- A1 ∈ {0, 1, 3} is independent of B1, giving 12 combinations.

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