**Ordering constraints from the sync points**
- A1–A5 happen before R, and B5 happens after R.
- A1–A7 happen before P, and B8–B9 happen after P.
- A1–A9 happen before Q, and B6–B7 happen after Q.
- B1–B4 have no sync constraints.
- So every A operation precedes B6 and B7. A8 and A9 may still come after B8 and B9.

**Writes to each block**
- Writes to z: A3 writes 5, B3 writes 3, A9 writes the value read by A6, B9 writes the value read by B2.
- Writes to x: A4 writes the value read by A2, B1 writes 5, B7 writes the value read by B2.
- B7 comes after Q, so it is after A5 and cannot affect A5.

**Possible values of individual reads**
- **A1** comes before A3, so it returns 0 or 3. It returns 3 only if B3 takes effect before A1.
- **A2** also comes before A3, so it returns 0 or 3.
- **A5** returns the value written by A4 (that is, A2's value). It returns 5 only if B1 takes effect between A4 and A5.
- **B2** comes before B3, so it returns 0, or 5 if A3 takes effect before B2.
- **A6** comes after A3 and before P, so before B9. It returns 5, or 3 if B3 takes effect between A3 and A6.
- **Final z** is set by whichever of A9 and B9 takes effect last. It equals A6's value if A9 is last, or B2's value if B9 is last.

**Case A1 = 0, A2 = 0** (B3 takes effect after A2)
- **A5 = 0:** B1 is not between A4 and A5. B2 can be 0 (B2 before A3) or 5. A6 can be 5 or 3. Final z can be 0, 3 or 5.
- **A5 = 5:** B1 is between A4 and A5, so B2 comes after A3 and B2 = 5. A6 can be 5 or 3. Final z can be 3 or 5.

**Case A1 = 0, A2 = 3** (B3 takes effect between A1 and A2)
- B2 comes before B3, which is before A3, so B2 = 0.
- B3 is before A3, so A6 = 5.
- B1 comes before B2, which is before A4, so B1 cannot fall between A4 and A5. Therefore A5 = 3.
- Final z is 0 or 5.

**Case A1 = 3**
- B3 takes effect before A1, so A2 = 3.
- The rest follows exactly as in the previous case: A5 = 3, B2 = 0, A6 = 5.
- Final z is 0 or 5.

BEGIN
0 0 0
0 0 3
0 0 5
0 5 3
0 5 5
0 3 0
0 3 5
3 3 0
3 3 5
END