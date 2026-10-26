Every possible outcome is listed between BEGIN and END, in the order A7, B6, final x, final z.

**Ordering constraints from the sync points:**
- A1, A2 and A3 all end before Q, and B2 starts after Q.
- A1 ends before S, and B3 starts after S, so A1 precedes B3.
- B1 to B4 end before R, and A4 starts after R.
- B1 to B6 end before P, and A9 starts after P. B7 and B8 are otherwise unconstrained.

**Facts that follow:**
- A3 reads 1. The only writes to z before Q are A1's, because B4 and B8 come after Q.
- B1 reads 0 or 4, but this does not affect the asked values.
- A6 writes 1 immediately before A7. So A7 reads 1, or 3 if B8 lands between A6 and A7. It cannot read 6.
- B6 comes after B3, so it cannot read 0. It reads 3 (B3's value), or A8's value if A8 ran early. A8 writes A7's value, so that would be 1.
- A9 always writes 1 to x, and B7 writes 5. Final x is 5 only if B7 comes after A9. Otherwise it is 1.
- Final z is 3 if B8 comes after A6, and 1 otherwise.

**Cases:**
1. **B6 = 1.** A8 wrote 1 before B6, so A7 = 1. B8 comes after B6, so it comes after A6, and final z = 3. Final x is 1 or 5. This gives (1,1,1,3) and (1,1,5,3).
2. **B6 = 3, A7 = 1.**
   - B8 comes early, before A4. A6 then overwrites it, so z = 1, and B7 is also early, so x = 1. This gives (1,3,1,1).
   - B8 comes after A7, so z = 3, and x is 1 or 5. This gives (1,3,1,3) and (1,3,5,3).
3. **B6 = 3, A7 = 3.** B8 sits between A6 and A7, so B7 is before A9. That gives x = 1 and z = 3, so (3,3,1,3).

BEGIN
1 1 1 3
1 1 5 3
1 3 1 1
1 3 1 3
1 3 5 3
3 3 1 3
END