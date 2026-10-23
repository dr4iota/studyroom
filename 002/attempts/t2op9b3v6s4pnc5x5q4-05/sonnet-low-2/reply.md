Every possible combination of A8, B2, B8 and B9 follows from the constraints below.

**Constraints**
- A1 and A2 end before P and R. B2 starts after P, and B3 comes after B2. So A2 reads z before any write to z, because B3, B4, B7 and A6 all come later. A2 returns 0, and A3 and A7 both write 0 to x.
- A1–A6 end before S, and B4–B9 start after S. So A5 (y=3) takes effect before B5.
- The only writes to y are A5 and B5, and A5 comes before B5. B5 writes B2's value, and B6 only reads y. So B9 always returns the same value as B2.
- The only writes to x are A1 (3), B1 (5), A3 (0) and A7 (0). B1 comes before B2 in program order.

**B2 (and B9)**
- B2 = 3: B1 is before A1, and B2 reads before A3. After that, only 0 is written to x, so B8 = 0 and A8 = 0.
- B2 = 0: B2 reads after A3 (or A7), and B1 is before that write. Then B8 = 0 and A8 = 0.
- B2 = 5: B1 is the last write to x before B2. There are three cases:
  - B1 comes before A3, which makes B8 = 0 and A8 = 0.
  - B1 comes between A3 and A7, and B8 reads before A7. This gives B8 = 5 and A8 = 0.
  - B1 comes after A7. Then B8 = 5, and A8 is 0 if it reads before B1, or 5 if it reads after B1.

Neither B8 nor A8 can be 3, because A1 is always overwritten by A3 before A6. A8 = 5 forces B1 after A7, which forces B8 = 5.

BEGIN
0 3 0 3
0 0 0 0
0 5 0 5
0 5 5 5
5 5 5 5
END