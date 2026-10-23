**Key constraints**

- C3 reads 2, and only A2 writes 2. So A2 must be the last write to x before C3.
- That forces C1 < C2 < A2 < C3. C2 writes 3, so it must come before A2.
- B3 (write 3) cannot fall between A2 and C3, so it is either before A2 or after C3.
- Program order gives A1 < A2 and B1 < B3.

**Possible values**

- A1 comes before A2 and can see 0, 1, or 3 (never 2).
- B1 comes before B3. It can see 0, 1, or 3 if B3 is late, and 2 only if it falls after A2 and B3 is after C3.
- The final value is 2 if B3 precedes A2, or 3 if B3 follows C3. Those are the only two possibilities, since C1 and C2 both precede A2.

**Cases**

- Final 2 (B3 before A2): B3 can sit before C1, between C1 and C2, or between C2 and A2. Across these placements, A1 ∈ {0,1,3} and B1 ∈ {0,1,3}. All 9 pairs are achievable. For example, (3,3) occurs with order C1, C2, B1, B3, A1, A2, C3.
- Final 3 (B3 after C3): A1 ∈ {0,1,3} and B1 ∈ {0,1,2,3}, giving 12 combinations.

That gives 21 outcomes in total.

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