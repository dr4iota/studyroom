**Ordering imposed by the sync points**
- B1–B5 all happen before P. A7 and A8 happen after P.
- A7 and A8 happen before Q. B7, B8 and B9 happen after Q.
- So: B1…B5 < P < A7, A8 < Q < B7, B8, B9.
- A1–A6 are not tied to thread B, apart from their own program order.
- A9 comes after A8, and also after R. R in turn comes after B1–B3.

**Q1: value returned by A9**
1. Every write of 1 to x (B2, B4) happens before P.
2. A8 writes 5 to x after P, and it is the only write to x before Q.
3. B8 runs after Q, so it reads 5. B9 therefore writes 5.
4. A9 runs after A8, so x is 5 whether A9 comes before or after B9.
5. So A9 always returns 5.

**Value read by A4 (call it v)**
- A1 and A2 write to y before A4, so A4 sees at least A2's 4.
- B5 (write 6 to y) may or may not take effect before A4.
- So v is 4 or 6.

**Case v = 6 (B5 took effect before A4)**
- Final y: A6 comes after A4, so after B5. Final y = 6.
- Final z: B3 comes before B5, so A5 comes after B3. Final z = 6.
- Result: y = 6, z = 6.

**Case v = 4 (A4 took effect before B5)**
- Final y: if A6 comes after B5, y = 4. If A6 comes before B5, y = 6.
- Final z: if A5 comes after B3, z = 4. If A5 comes before B3, z = 6.
- All four mixes are possible:
  - y = 6, z = 4: order B3 < A5 < A6 < B5.
  - y = 4, z = 6: order A5 < B3 < B5 < A6.
  - y = 4, z = 4: order B3 < A5 < B5 < A6.
  - y = 6, z = 6: order A5 < A6 < B3 < B5.

BEGIN
5 4 4
5 4 6
5 6 4
5 6 6
END