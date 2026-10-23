Only the writes to y matter for the constraints, so I start there.

**Writes to y:** A1 writes 5, B1 writes 4, and C3 writes the value C2 read.

**Constraints from the known reads:**
- B3 returns 4, so the last write to y before B3 is B1. Since B1 comes before B3, A1 is not between B1 and B3.
- B5 returns 2, so the last write to y before B5 is C3, and C3 wrote 2. This means C2 read 2, and C3 comes after B1, A1 and B3.
- A3 returns 4, so the last write to y before A3 is B1. Hence A1 < B1 < A3, and A3 comes before C3, because C3 would otherwise overwrite y with 2.
- The order is therefore A1 < B1 < {A3, B3} < C3 < B5.

**Q1 (A2 reads z):** The only write to z is C5, and it comes after C3. A2 comes before A3, which comes before C3, so A2 reads 0.

**Q4 (final y):** Every write to y (A1, B1, C3) happens before B5, and C3 was the last one before B5. The final value of y is 2.

**Q2 and Q3 (C4 and final x):** The writes to x are C1 (2), B2 (3) and B4 (3). C2 read 2, so neither B2 nor B4 landed between C1 and C2. C4 comes after C1, so it reads 2 or 3, and the final x depends on which write is last.
- C4 = 2, final x = 2: C1 is the last write to x, after B2 and B4.
- C4 = 2, final x = 3: B4 comes after C4.
- C4 = 3, final x = 3: B4 lands between C3 and C4.
- C4 = 3, final x = 2 is impossible. C4 would have to see a B write after C1, and no later write could bring x back to 2, because C1 has already happened.

BEGIN
0 2 2 2
0 2 3 2
0 3 3 2
END