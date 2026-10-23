**Answers:** A8 ∈ {0, 5}, B2 ∈ {0, 3, 5}, B8 ∈ {0, 5}, and B9 always equals B2. This gives five combinations.

**1. A2 always reads 0.**
- The only writes to z are B3, B4 and B7.
- All three come after P, and A2 comes before P.
- So A3 and A7 both write 0 to x.

**2. B9 always equals B2.**
- B9 comes after Q, so A5 (write 3 to y) has already taken effect.
- B5 comes after S, and A5 comes before S, so B5 takes effect after A5.
- B5 also comes before B9 in thread B.
- So the last write to y before B9 is B5, which writes B2's value.

**3. The writes to x are:**
- A1 writes 3, before P.
- A3 and A7 each write 0.
- B1 writes 5. Its only constraint is that it comes before B2.

**4. Cases by the value B2 returns:**

- **B2 = 3:**
  - The order must be B1 < A1 < B2 < A3.
  - B8 comes after Q, so after A3. Every write to x after A3 writes 0, so B8 = 0.
  - B1 is already before A3, so A8 reads A7's 0.
  - Result: (0, 3, 0, 3).

- **B2 = 5:** nothing writes x between B1 and B2.
  - If B1 falls between A7 and A8, then A8 = 5 and B8 = 5.
  - If B1 comes after A8, then A8 = 0 and B8 = 5.
  - If B1 and B2 both come before A3, then A8 = 0 and B8 = 0.
  - Results: (5, 5, 5, 5), (0, 5, 5, 5) and (0, 5, 0, 5).

- **B2 = 0:**
  - B1 must come before A3 or A7, and B2 must come after that write.
  - So no write of 5 follows, and A8 = 0 and B8 = 0.
  - Result: (0, 0, 0, 0).

BEGIN
0 3 0 3
5 5 5 5
0 5 5 5
0 5 0 5
0 0 0 0
END