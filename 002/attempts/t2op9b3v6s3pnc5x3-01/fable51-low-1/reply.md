**Analysis**

- **Q1 (A9):** All writes to x are B2(1), B4(1), A8(5), B9. B4 is before P, A8 is after P, so A8 is the last of the "fixed" writes. B8 happens after Q (hence after A8) and reads 5, so B9 also writes 5. A9 is after A8, so it returns 5 in every execution.
- **Q2 (final y):** Writes to y are A1(5), A2(4), A6(A4's value), B5(6), all before P. A4 returns 4 or 6; A6 rewrites that value. Final y is 4 (A6 writes 4 after B5) or 6 (A6 writes 6, or B5 comes after A6).
- **Q3 (final z):** Writes to z are A3(1), A5(A4's value), B1(2), B3(6). The last write is A5 (4 or 6) or B3 (6), so final z is 4 or 6. Each combination with y is realizable (e.g., y=6, z=4: A4 reads 4, B3 before A5, B5 after A6).

BEGIN
5 4 4
5 4 6
5 6 4
5 6 6
END