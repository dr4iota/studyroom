Neither thread has sync points, so every interleaving that keeps each thread's own order is allowed. Write a for the value A1 reads and b for the value B4 reads.

**Q1 (A1):** A1 can read 0, 1 or 3.
- It reads 0 if it runs before B1.
- It reads 1 if it runs between B1 and B2.
- It reads 3 if it runs after B2. B3 must still read 3, so B3 must come before A2 or after A5.
- A1 cannot read 2, because A2 comes after A1.

Each of these values is consistent with B3 returning 3.

**Writes to y:** There are three: A3 writes a, B5 writes 2, and B6 writes b. B4 comes before B5, so b is either 0 or a, depending on whether A3 came first. Since B6 comes after B5, the final y is either a (A3 last) or b (B6 last). The final y is never 2.

**Q2 (A4):** A4 runs after A3, so it can read:
- a, from A3 or from B6 with b = a.
- 2, from B5.
- 0, from B6 with b = 0. This needs B4 < A3 < B6 < A4.

**Case a = 0:**
- A4 is 0 or 2, and the final y is 0.

**Case a = 1 or a = 3:**
- A4 = a: final y is a (A3 or B6 with b = a is last). Final y is 0 if B4 < A3 < A4 < B5 < B6.
- A4 = 2: B5 falls between A3 and A4, so B6 comes after A3. The final y is b, which is 0 if B4 < A3, or a if B4 > A3.
- A4 = 0: B6 writes 0 before A4, so the final y is 0.

Each of these orderings is consistent with B3 = 3.

BEGIN
0 0 0
0 2 0
1 1 1
1 1 0
1 2 0
1 2 1
1 0 0
3 3 3
3 3 0
3 2 0
3 2 3
3 0 0
END