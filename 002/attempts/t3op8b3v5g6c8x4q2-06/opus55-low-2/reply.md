**Answer:** Q1 (A4) can be 0 or 3, and Q2 (final z) is always 2.

**1. How A6 can return 0.** A1 writes 2 to z before A6, so some later write must put 0 back into z. The only candidate is B6, which writes the value read by B1. So B1 must return 0, and B6 must take effect between A5 and A6.

**2. Consequences of B1 returning 0.**
- B1 reads x before A2, C1, C3 and C6 write to x.
- B5 then writes 0 to y.
- The final y = 1 means C7 takes effect after B5.

**3. Ordering of the z writes.**
- The writes to z are A1(2), A5(4), C5(4), B6(0), A7(3, because A3 returned 3) and A8(2).
- B2 and B3 return 2, and both come before B6, which comes before A6, which comes before A8.
- So their value must come from A1. That puts both A5 and C5 after B3.

**4. Ordering of the x accesses.**
- B4 returns 1, so B4 comes after A2 and before the next write of 3 to x.
- A3 returns 3, so a C write of 3 (C1 or C3) falls between B4 and A3.
- B7 returns 3, and it comes after B6. So C6 (writes 4 to x) takes effect after B7.

**5. Final z (Q2).**
- C8 returns 2. C5 comes before C8, so the last z write before C8 must be A8.
- Every other z write comes earlier: B6 is before A6, and C5 is before C8.
- So A8 is the last write to z, and the final z = 2.

**6. Value returned by A4 (Q1).** The writes to y are C2(3), B5(0) and C7(1).
- **1 is impossible.** C7 comes after C6, which comes after B7, B6 and A5. A5 comes after A4, so C7 is always after A4.
- **0 is possible.** For example, A4 reads before both C2 and B5. Alternatively, B5 writes 0 after C2 and before A4.
- **3 is possible.** C2 takes effect before A4, and B5 takes effect after A4.

BEGIN
0 2
3 2
END