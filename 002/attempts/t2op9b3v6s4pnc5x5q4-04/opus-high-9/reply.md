**Answer:** B9 always equals the value B2 read, and that is also the final z. B2 sees either 0 or A8's write, which is 1 or 6. The final x is 1 only when B2 reads 0. That gives six combinations.

**Ordering constraints from the sync points:**
- B1 < P < A3
- B1, B2 < Q < A9
- A1 < S < B5
- All of A < R < B8, B9

**z, and the value of B9.** Every A write to z (A1, A6, A9) happens before R. B8 happens after R. B8 writes the value B2 read, and nothing writes z after it. So B9 equals B2's value, and the final z equals B2's value.

**A4 and A7.**
- Both B1 and A1 happen before A4. So A4 reads 6 if B1 took effect before A1, and 1 if B1 came after A1. Both orders are allowed.
- A6 writes A4's value to z, and A7 reads z next. Between A6 and A7 nothing else can write z: B1 is already before A3, A9 comes later, and B8 is after R. So A7 = A4's value, which is 1 or 6.

**y.** A8 is the only write to y, so the final y is v, where v is 1 or 6 (A4's value).

**B2.** B2 reads y and must happen before Q, which is before A9. B2 can read 0 if it comes before A8. It can read v if it comes after A8; the order B1 < P < A3 … A8 < B2 < Q < A9 is allowed.

**x.**
- B7 writes 4 after B5, which is after S. A2 is not ordered against S, so A2 may come after B7. In that case the final x is 1; otherwise it is 4.
- If B2 reads v, then A2 < A8 < B2 < B7, so the final x must be 4.
- If B2 reads 0, either value of x is possible. For example, B1, A1, S, B2…B7, A2, P, A3… gives x = 1 with v = 6. Swapping A1 and B1 gives x = 1 with v = 1.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END