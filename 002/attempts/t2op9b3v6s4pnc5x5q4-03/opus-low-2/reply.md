**Constraints from the sync points**
- B1–B3 happen before R, and A2 happens after R. So B1 happens before A2.
- B4 happens before P and before Q. A2 happens after Q and A3 happens after P. So B4 happens before A2 and A3.
- B5 happens before S, and A8 happens after S. So B5 happens before A8.

**Value read by B2 (v₂)**
The writes to x are B5, A4, A5 and A6. B5 comes after B2 in thread B. A4–A6 happen after P, which is after B4, which is after B2. So no write to x takes effect before B2, and B2 returns 0. Therefore B9 writes 0 to y.

**Value read by A2 (v)**
The writes to y are B1 (6), B8 (6) and B9 (0). B1 is always before A2.
- If B9 takes effect before A2, then v = 0.
- Otherwise the last write before A2 is B1 or B8, and v = 6.

**Final z**
B4 (writes 3) takes effect before A3, which writes v. No write to z comes after A3. So final z = v.

**A8 and final x**
- A8 returns v if B5 takes effect before A6.
- A8 returns 4 if B5 takes effect after A6.
- No write to x follows A8, so final x equals A8's value.

**A9**
A9 returns 0 if B9 takes effect before A9. It returns 6 if B9 takes effect after A9, because B1 has already happened.

**Case v = 0**
- B9 is before A2, so A9 = 0.
- B5 is before B9, which is before A2, which is before A6. So A8 = 0 and final x = 0.
- Result: 0 0 0 0.

**Case v = 6**
- B9 is after A2, so A9 can be 6 or 0.
- B5 can be on either side of A6, so A8 can be 6 or 4, with final x equal to A8.
- These choices are independent, which gives four combinations. Final z = 6 in each.

BEGIN
6 6 6 6
6 0 6 6
4 6 4 6
4 0 4 6
0 0 0 0
END