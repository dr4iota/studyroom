Thread A's operations A2 through A8 must all come after every operation of thread B, because B8 happens before Q and Q happens before A2. A1 can fall at any of nine positions among B's operations, since it only needs to precede A2.

Let k be the number of B operations before A1:

- **B2** reads x = 0, and **B3** reads y = 1 if k ≤ 2, otherwise 0. So b3 = 1 for k ≤ 2 and 0 otherwise.
- **B8** reads y. B7 writes 6 to y just before it, so the read gives 6, except when A1 falls between B7 and B8 (k = 7), where it gives 1.
- **A2** reads x, which holds b3 from B5, so a2 = b3.
- **A3** writes 2 to z, so **A7** reads z = 2.
- **A4** writes a2 to y and **A5** writes a2 to x, so **A6** returns b3 and **A8** returns b3.

So Q1 = 2 always, Q2 = b3, and Q3 = b8. The cases are:

- k = 0, 1, 2: b3 = 1, b8 = 6
- k = 3 to 6, and k = 8: b3 = 0, b8 = 6
- k = 7: b3 = 0, b8 = 1

Q1 Q2 Q3 can therefore be (2, 1, 6), (2, 0, 6), or (2, 0, 1).

BEGIN
2 1 6
2 0 6
2 0 1
END