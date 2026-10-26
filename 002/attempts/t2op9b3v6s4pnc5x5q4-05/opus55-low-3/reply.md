**Fixed facts**

1. **A2 returns 0.** Every write to z (B3, B4, B7) comes after P, and A2 comes before P. So A3 and A7 both write 0 to x.

2. **B9 equals B2.** The y-writes are A5 (writes 3) and B5 (writes B2's value). A5 is before S and B5 is after S, so B5 takes effect after A5. B9 comes after both (B5 is earlier in thread B, and A5 is before Q). So B9 reads B5's value, which is B2's value.

3. **B2 reads x after A1.** A1 is before P and B2 is after P. B1 also comes before B2. The candidates are 3 (A1), 5 (B1) or 0 (A3 or A7).

**Case B2 = 0**
- An A-write of 0 (A3 or A7) takes effect after B1 and before B2.
- B8 comes later, and nothing writes x after that 0 except possibly the other 0-write. So B8 = 0.
- A8 must also be 0, because A8 = 5 would need B1 after A7.
- Result: **0 0 0 0**.

**Case B2 = 3**
- Order: B1 < A1 < B2 < A3.
- A8 can only be 0, since B1 is before A3 and A7.
- B8 is after Q, so after A3. Both A3 and A7 write 0, so B8 = 0.
- Result: **0 3 0 3**.

**Case B2 = 5**
B1 takes effect after A1 and is the last write before B2. Three orders work:
- **A3 after B1:** A8 = 0 and B8 = 0. Result: **0 5 0 5**.
- **A3 < A7 < A8 < B1 < B2:** A8 = 0, B8 = 5. Result: **0 5 5 5**.
- **A7 < B1 < A8:** A8 = 5 and B8 = 5. This fits because B1 only has to come before B2, which comes before B3 and S. A3 to A6 can come before S while A7 and A8 do not. Result: **5 5 5 5**.

BEGIN
0 0 0 0
0 3 0 3
0 5 0 5
0 5 5 5
5 5 5 5
END