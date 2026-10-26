**Approach.** A3 writes 2 to x before A5, but A5 reads 0. So some write of 0 to x must take effect after A3 and before A5. The only candidates are B4 and C5, and each writes back a value read from x. The value of x is only ever 0 or 2, so B2 and C3 each return 0 or 2. At least one of them must return 0, and the matching write (B4 or C5) must supply the 0 inside the window from A3 to A5.

The final z is set by whichever of A4 (1), B1 (5) or C2 (1) takes effect last. C1 always comes before C2, so it can never be last. The final z is therefore 1 or 5, and it is 5 only if B1 can come after both A4 and C2.

**Case B2 = 0, C3 = 2**
- C3 reads 2, so C5 writes 2. The 0 must come from B4.
- B2 read 0. The only possible 0-write after A3 is C5, which writes 2 here. So B2 must take effect before A3.
- That puts B1 before B2, before A3, before A4. So B1 cannot be last.
- Example: B1, B2(0), A1, A2, C1, C2, A3, C3(2), C5, B4(0), A4, A5, B3, C4.
- Final z is **1** only.

**Case B2 = 2, C3 = 0**
- C3 must read 0 before A3, and C2 comes before C3.
- B2 reads 2 after A3. B4 then writes 2, and C5 writes 0 after B4 and before A5.
- B1 can be placed after A4: C1, C2, C3(0), A1, A2, A3, A4, B1, B2(2), B4(2), C5(0), A5, B3, C4. This gives final z = **5**.
- Placing A4 last instead gives final z = **1**.

**Case B2 = 0, C3 = 0**
- With B2 before A3, B1 comes before A4. Then A4 or C2 is last, so z = **1**.
- B2 can also read 0 after A3, because C5 has already written 0 by then. Order: C1, C2, C3(0), A1, A2, A3, C5(0), A4, B1, B2(0), A5, B3, B4, C4.
- A5 reads 0 as required, and B1 is the last write to z, so z = **5**.

BEGIN
0 2 1
2 0 1
2 0 5
0 0 1
0 0 5
END