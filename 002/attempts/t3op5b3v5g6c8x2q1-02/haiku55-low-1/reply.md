Final y can be **2** or **5**.

**Key deductions:**

1. **z is always 5 once read.** The only write to z is A1 (value 5). B2 and C2 both read 5, so A1 takes effect before both. B3 comes after B2, so B3 also reads 5. Therefore B4 writes 5 to y and B5 writes 5 to x.

2. **A3 reads y = 4.** The only write of 4 is C4, so C4 is the last write to y before A3. No other y-write (including B4, which writes 5) can fall between C4 and A3.

3. **A2 reads y = 1.** The only write of 1 is C1, and B4 writes 5, so C1 must be the last y-write before A2. This forces C1 < A2 < C4 < A3.

4. **C3 reads x = 1.** This requires B1 < C3 < B5.

5. **Final y.** A4 comes after A3, which comes after C4, so C4 is never the last write to y. The candidates are A4 (writes 2) and B4 (writes 5). B4 can be placed after A3, so it can come after A4 as well.

**Both outcomes are achievable:**

- Final y = 2: A1, B1, B2, C1, C2, A2, C3, C4, A3, B3, B4, B5, A4. Here A4 is last on y.
- Final y = 5: the same order but with B4 moved after A4. B4 writes 5 last on y.

BEGIN
2
5
END