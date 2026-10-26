**Ordering constraints from the sync points**
- B1 < P < A3. Thread A's steps from A3 onward come after P.
- B2 < Q < A9.
- A1 < S < B5.
- A9 < R < B8.

**Values read in thread A**
- **A4 (reads z):** Both z-writes A1 (6) and B1 (1) happen before A4, since B1 < P < A3 < A4. Their relative order is free. So A4 = v, with v ∈ {1, 6}.
- **A7 (reads z):** The last z-write before A7 is A6, which writes v. B8 cannot come earlier, because it is after R. So A7 = v.

**Final y**
- A8 is the only write to y, and it writes A7's value. So final y = v.

**B2 (reads y)**
- B2 and A8 are both before Q, and their order is free.
- So B2 is either 0 (B2 before A8) or v (A8 before B2).

**Final z and B9**
- B8 writes B2's value to z after R.
- Every z-write in thread A is before R.
- So B9 and the final z both equal B2's value, which is 0 or v.

**Final x**
- B7 writes 4, and A2 writes 1.
- A2 only has to come after A1 and before A3. B7 only has to come after S and before B8.
- Nothing forces an order between A2 and B7, so final x is 1 or 4.
- B6's value is always overwritten by B7, so B3 does not matter.

**Combining**
- Final x ∈ {1, 4}, independent of the rest.
- v ∈ {1, 6}.
- B9 = final z ∈ {0, v}.

This gives 2 × 2 × 2 = 8 combinations.

BEGIN
0 1 1 0
0 1 6 0
1 1 1 1
6 1 6 6
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END