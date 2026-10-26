The final value of y can only be **1**.

**Writes to y.** Only A3 (writes 1) and B2 (writes 4) write to y. So the final y is 1 if A3 takes effect after B2, and 4 if B2 takes effect after A3.

**Final y = 1 is possible.** One valid order is:
B1, B2, B3, B4, C1 (reads 3), C2 (reads 3), C3, C4 (writes 3 to x), C5, A1, A2, A3, A4, A5.
- C2 reads 3 because B1 wrote 3 to z.
- A2 is the last write to x, so x ends at 4.
- A3 comes after B2, so y ends at 1.

**Final y = 4 is impossible.**
1. If y ends at 4, then B2 comes after A3. A2 comes before A3, and B3 and B4 come after B2, so B3 and B4 both come after A2. That means A2 is not the last write to x.
2. The final x = 4 must then come from C4 being the last write to x, so C1 must have returned 4.
3. C1 can return 4 only if A5 wrote 4 to z before C1. That needs A4 to have read 4, so the order is B2, then A4, then A5, then C1.
4. C2 comes after C1, so it also comes after A5. The only write of 3 to z before C2 is B1. B1 comes before B2, so it comes before A5. C3 writes 3, but only after C2.
5. So the last write to z before C2 is A5's 4, and C2 cannot return 3. This contradicts the known result.

BEGIN
1
END