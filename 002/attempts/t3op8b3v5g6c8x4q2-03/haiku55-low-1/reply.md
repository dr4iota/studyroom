**Key deductions**

- **Final y** is the later of A5 (writes 2) and B7 (writes v4), so it is 2 or v4.
- **Final z** is the later of B8 (writes v4) and C8 (writes v2), so it is v4 or v2.
- **v4 = 3.** After C4 writes 4, C6 must read 3, so the last z-write before C6 must be B5 or B8 writing v4, and that must equal 3.
- **v7 ∈ {2, 3}.** A7 follows A6, which reads 2, so the only possible later y-writes are B1 and B7, both 3.
- **v2 ∈ {1, 2, 3, 5}.** B2 writes 5 to x, and B2 precedes C2 in every valid order. Option A (B3 < C1 < B4) is the only way for B4 to read 3 unless v2 = 3, so v2 = 0 is impossible.
- **(2, 2) is impossible.** Final y = 2 forces B7 < A5, so v7 = 2. Then v2 = 2 requires A8 to be the last x-write before C2, which places C2 before C5. C7 would then need an x-write of 3 after C5, and none exists.

**Witness schedules** (positions 1–24 in time order)

- **(2, 1):** B1, B2, B3, C1, A1, B4, C2 (reads 1), A2, A3, C3 (z=1), C4, B5, C5, C6, B6, C7, B7, A4, A5, A6, A7, A8, B8, C8 (z=1). Final y=2, z=1.
- **(2, 3):** B1, B2, B3, C1, A1, A2, A3, B4, C2 (reads 3), C3, C4, B5, C5, C6, C7, B6, B7, A4, A5, A6, A7, A8, B8, C8. Final y=2, z=3.
- **(2, 5):** B1, B2, B3, C1, B4, C2 (reads 5), C3, C4, B5, C5, C6, A1, A2, A3, B6, C7, B7, A4, A5, A6, A7, A8, B8, C8 (z=5). Final y=2, z=5.
- **(3, 1), (3, 3), (3, 5):** the (2, ·) schedules with A4, A5, A6 moved before B7, so B7 writes 3 last to y. Final z is 1, 3, or 5 as before.
- **(3, 2):** B1, B2, B3, C1, A1, A2, A3, B4, A4, A5, A6, A7, A8 (x=2), C2 (reads 2), C3, C4, B5, C5, C6, B6, C7, B7, B8, C8 (z=2). Final y=3, z=2.

BEGIN
2 1
2 3
2 5
3 1
3 2
3 3
3 5
END