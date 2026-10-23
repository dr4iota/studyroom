Constraints from the sync points: A1–A5 finish before R. A6 and A7 come after R and before P. A8 and A9 come before Q. B5 comes after R. B6 and B7 come after Q, and B8 and B9 come after both P and Q, so all of B6–B9 come after every A operation.

**Q1 (A1).** A3 is the only write of 5 to z, and it comes after A1. The only other write to z before A3 is B3, which writes 3. So A1 is 0 or 3. A2 is also 0 or 3 and cannot be lower than A1 in time order, giving (A1,A2) = (0,0), (0,3) or (3,3).

**Q2 (A5).** A4 writes A2's value to x, and B1 writes 5 to x. B7 is after Q, so it cannot affect A5.
- If A2 = 3, then B1 and B3 both happened before A2, so A5 = 3.
- If A2 = 0, then B3 comes after A2. A5 is 0 if B1 is not between A4 and A5, and 5 if it is.

**Q3 (final z).** B9 is the last write to z, so the final value of z is whatever B2 read. B2 reads z before B3 writes 3, so B2 sees 0, 5 (from A3), or the value A9 wrote (3 or 5). B2 cannot see 3, because B2 comes before B3, and 3 can only reach z through B3 or through A9, which needs B3 first. So the final z is 0 or 5.
- Final z = 5 requires B2 to read 5, which means B2 is after A3 and B3 is after A3. Then A1 = A2 = 0, so A5 is 0 or 5.
- Final z = 0 requires B2 to read 0, so B2 is before A3. Then B1 is before A3 and cannot fall between A4 and A5, so A5 ≠ 5. A5 is 0, or 3 when B3 precedes A2.

Combinations (A1, A5, final z):
- (0, 0, 0)
- (0, 3, 0)
- (3, 3, 0)
- (0, 0, 5)
- (0, 5, 5)

BEGIN
0 0 0
0 3 0
3 3 0
0 0 5
0 5 5
END