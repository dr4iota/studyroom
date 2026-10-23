**How the known results constrain the order**

- **B5 reads z = 4.** The only write to z is A3, so A3 takes effect before B5. A2 reading 0 fits, because A2 comes before A3.
- **B1 reads x = 0.** So B1 takes effect before B2 and before A5, which writes 3.
- Each thread keeps its own order: A1 < A2 < A3 < A4 < A5 and B1 < B2 < B3 < B4 < B5.

**Values of x along thread B**

| Stage | Interval | Value of x |
|---|---|---|
| 0 | before B2 | 0 |
| 1 | after B2 | 2 |
| 2 | after B3 | 1 |
| 3 | after B4 | 2 |

A5 is the only write in A that could change x before A4, and it comes after A4. So A1 and A4 each read the value of the stage they fall in.

**Where A1 and A4 can fall**

- A1 can be in any stage. It only needs A1 < A3 < B5, and B4 is also before B5.
- A4 can be in any stage at or after A1's stage. Even stage 0 works for A4: A4 then falls before B2, and A3 before it still precedes B5.

**Final value of x**

- If A4 is in stage 3, A5 comes after B4, so x ends as 3.
- If A4 is in stage 0, 1 or 2, A5 can take effect before B4 (x ends as 2) or after it (x ends as 3). A5 still comes after B1 in both cases.

**Combinations**

- **A4 in stage 3 (reads 2):** A1 reads 0, 2 or 1, and x ends as 3.
- **A4 in stage 2 (reads 1):** A1 reads 0, 2 or 1, and x ends as 2 or 3.
- **A4 in stage 1 (reads 2):** A1 reads 0 or 2, and x ends as 2 or 3.
- **A4 in stage 0 (reads 0):** A1 reads 0, and x ends as 2 or 3.

BEGIN
0 0 2
0 0 3
0 1 2
0 1 3
1 1 2
1 1 3
2 1 2
2 1 3
0 2 2
0 2 3
1 2 3
2 2 2
2 2 3
END