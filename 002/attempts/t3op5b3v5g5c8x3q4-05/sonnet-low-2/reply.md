Every combination has Q1 = 0 and Q4 = 2. The reasoning is below.

**Fixing C2.**
- B5 reads y = 2, and only C3 can write a 2 to y. So C3 writes 2, which means C2 returned 2.
- Therefore C5 also writes 2 to z.

**Ordering the writes to y.**
- B3 reads 4, so B1 takes effect before B3. No other write to y may fall between B1 and B3. A1 writes 5 and C3 writes 2, so neither can.
- B5 reads 2, so C3 is the last write to y before B5.
- Together this gives B1 < B3 < C3 < B5.
- A1 must also avoid the window between C3 and B5.

**Placing A1.**
- A3 reads 4 and comes after A1 in thread A.
- If A1 fell between B3 and C3, y would be 5 until C3 and then 2, so A3 could never read 4.
- If A1 came after B5, y would never be 4 again, so A3 could not read 4.
- So A1 comes before B1, and A3 reads 4 in the window between B1 and C3.
- C3 is then the last write to y, so the final y is 2 (Q4).

**Q1.**
- A2 comes before A3, and A3 takes effect before C3.
- C5 comes after C3, so C5 cannot have taken effect yet. A2 therefore reads 0.

**Q2 and Q3.**
- C1 writes 2 and takes effect before C2, with no write of 3 in between, so C2 reads 2.
- C4 comes after C3 and reads either 2 or 3.
- (C4 = 2, final x = 2): B2 and B4 both take effect before C1, and C1 is the last write to x.
- (C4 = 2, final x = 3): B4 takes effect after C4.
- (C4 = 3, final x = 3): B2 or B4 takes effect after C2 and before C4.
- (C4 = 3, final x = 2) is impossible. C1 takes effect before C2, so a 3 read by C4 comes from a later write, and that write would leave the final x at 3.

BEGIN
0 2 2 2
0 2 3 2
0 3 3 2
END