**Fixed facts**

1. A1–A5 happen before S, and every step of B happens after S. So A4 reads y before anything writes y. A4 returns 0.
2. B1 also sees no write to y, so B1 returns 0. That means B3 writes 0 to z and B4 writes 0 to y.
3. A6 writes 0 to z and A8 writes 0 to x.
4. The ordering chain is B1 < R < A8 < A9 < P < B9. Also B2 < B4 < Q < A9.

**Consequences**

- A9 always comes after B2. Only B2 (4) and A8 (0) can be the latest write to x before A9, because B9 comes after P. So A9 returns 0 if B2 comes before A8, and 4 if A8 comes before B2.
- B5 comes after B2. It returns 0 if A8 lies between B2 and B5, and 4 otherwise.
- B8 comes after B5. It returns 0 if A8 comes before B8, and 4 otherwise.
- The final value of x is B9's write, which equals B5's result.
- B6 (1) comes after B3, so B3 never decides z. The final value of z is 0 if A6 comes after B6, and 1 otherwise.

**Cases**

- **A8 < B2:** A9 = 4, B5 = 4, B8 = 4, final x = 4. Since A6 < A8 < B2 < B6, final z = 1.
- **B2 < A8 < B5:** A9 = 0, B5 = 0, B8 = 0, final x = 0. Since A6 < A8 < B5 < B6, final z = 1.
- **B2 < B5 < A8:** A9 = 0, B5 = 4, final x = 4.
  - B8 is 4 if B8 comes before A8, and 0 if it comes after.
  - B6 may fall before A6, and both stay before A8. So final z can be 0 or 1 for either value of B8.
  - Example for B8 = 0 with z = 0: B5 < B6 < A6 < A8 < B8.

BEGIN
4 4 4 1
0 0 0 1
0 4 4 0
0 4 4 1
0 0 4 0
0 0 4 1
END