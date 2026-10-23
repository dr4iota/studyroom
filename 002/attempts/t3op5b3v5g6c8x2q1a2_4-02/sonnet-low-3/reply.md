Only two final values of y are possible: 2 and 5.

**Value of B3.** The only write to z is A1, which writes 5. B2 returned 5, so A1 took effect before B2. B3 comes after B2, so B3 also reads 5. Therefore B4 writes 5 to y and B5 writes 5 to x.

**Writes to y.** The writes are C1 (1), C4 (4), B4 (5) and A4 (2).

**Ordering constraints.**
- A2 read 1. The only write of 1 to y is C1, so C1 took effect before A2.
- A3 read 4. The only write of 4 to y is C4, so C4 was the last write to y before A3.
- C4 cannot take effect before A2. C1 comes before C4, so y would already be 4 (or later overwritten, but never back to 1), and A2 would not read 1. So C4 falls between A2 and A3.
- A4 comes after A3 in thread A, so A4 comes after C4.
- Reading x as 1 in C3 only needs B1 to come before C3.
- Reading z as 5 in C2 only needs A1 to come before C2.

**Final value.** The last write to y is one of A4, B4 or C4. C4 is always before A3, which is before A4, so C4 cannot be last, and 4 is ruled out. B4 is only constrained to come after B3, so it can fall either side of A4:
- If A4 is last, the final value is 2.
- If B4 is last, the final value is 5.

Both orderings are consistent with all the known read results.

BEGIN
2
5
END