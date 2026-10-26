Block y is written only by A3 (value 4) and C4 (the value C3 read), so the possible values follow from the orderings of those writes.

**Q3 (C3):** Before C4 runs, A3 is the only write to y. So C3 returns 0 if A3 hasn't taken effect yet, or 4 if it has.

**Q1 (A2):** A2 comes before A3 in thread A. C4 comes after C3, and C3 reads 4 only if A3 has already happened. So at the time A2 reads y:
- If C3 = 0, C4 writes 0 to y, so y holds only 0 or the untouched initial 0.
- If C3 = 4, A3 precedes C3, so A2 precedes C4. y is still 0.

In both cases A2 returns 0.

**Q2 (A4):**
- A1 returned 3, so C1 already took effect. A4 therefore cannot return 0 from the initial state. It can return 3, 4 (from B1), or C4's value.
- C3 = 0: A4 can be 3, 4 or 0.
  - A4 = 3: B1, then C1, C2, A1, C3, A2, A3, A4.
  - A4 = 4: C1, C2, A1, C3, A2, A3, B1, A4.
  - A4 = 0: B1, C1, C2, A1, C3, C4, A2, A3, A4, with C4 writing 0 to x.
- C3 = 4: C4 writes 4, so A4 can be 3 or 4.
  - A4 = 3: B1, C1, C2, A1, A2, A3, A4, C3, C4.
  - A4 = 4: any ordering where B1 (or C4) lands before A4 and the last write to x before A4 is 4.
  - A4 = 0 is impossible, because C4 would write 4.

BEGIN
0 3 0
0 4 0
0 0 0
0 3 4
0 4 4
END