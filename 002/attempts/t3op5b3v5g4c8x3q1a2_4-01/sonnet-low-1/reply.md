B4 can return only 0 or 4.

**Facts forced by the known results**
- B5 reads z as 0, and C5 is the only write to z, so C5 takes effect after B5. B1 comes before B5 in B's order, so B1 also reads 0. B3 therefore writes 0 to x.
- A2 reads x as 3. That requires C2 to be the last write to x before A2, so C2 precedes A2, and B3 is not between C2 and A2.
- y only ever holds 0, 4 or 3. A1 and C4 write 4, and A4 writes whatever A3 read from z (0 or 3).
- B2 reads y as 4 before B4, so y has already been 4 by then.

**Which values B4 can return**
- **3 is impossible.** A4 can write 3 only if A3 read z as 3, which needs C5 to have taken effect. C5 comes after B5, which comes after B4, so B4 cannot see that write.
- **4 is possible.** Leave y at 4 from A1 and C4, with A4 not yet run.
- **0 is possible.** Use this order of effects:
  1. A1, C1, C2, A2 (reads 3)
  2. A3 (reads z as 0)
  3. B1 (reads 0), B2 (reads y as 4)
  4. B3 (writes 0 to x, after A2, so A2 is unaffected)
  5. C3 (reads y as 4)
  6. A4 (writes 0 to y)
  7. B4 (reads 0)
  8. B5 (reads 0), C4, C5

  Every known result holds in this order.

BEGIN
0
4
END