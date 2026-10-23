**Key deductions**

- A3 runs after A1 (same thread) and before Q, while every other z‑write (B4, B8, A4–A6) comes after Q, so A3 returns 1.
- A7 reads z after A6 (which wrote 1); the only other write that can interleave is B8 (3), which may land before A4, between A6 and A7, or after A7. So A7 ∈ {1, 3}.
- B6 reads x after B3 (3) and before P, hence before A9 and B7; it can only see 3 or A8's value (A8 = A7). So B6 ∈ {3, A7}.
- Final x is A9 (1) or B7 (5), both after P, either order.
- Final z is A6 (1) or B8 (3).

Constraints between them:
- A7 = 3 ⇒ B8 came after A6 ⇒ final z = 3, and B6 < P < B8 < A7 < A8 ⇒ B6 = 3.
- A7 = 1, B6 = 1 ⇒ A8 < B6 < P < B8, and A6 < A8 ⇒ final z = 3.
- A7 = 1, B6 = 3 ⇒ B8 either before A4 (final z = 1) or after A7 (final z = 3).
- Final x is independent in all cases.

BEGIN
1 1 1 3
1 1 5 3
1 3 1 1
1 3 5 1
1 3 1 3
1 3 5 3
3 3 1 3
3 3 5 3
END