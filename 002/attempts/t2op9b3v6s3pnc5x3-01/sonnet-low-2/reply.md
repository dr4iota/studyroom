A9 always reads 5, the final value of y is 4 or 6, and the final value of z is 4 or 6, with all four y/z pairings possible.

**Ordering constraints**
- B1–B5 all end before P, since B3 is before R and the "before P" line sits under B5.
- A7 and A8 start after P, and A8 ends before Q.
- B7–B9 start after Q.
- B6 is only ordered after B5.
- A1–A6 are only ordered before A7.

**Q1: A9**
- B4 is the last write to x before A8 (B4 ends before P and A8 starts after P). A8 then writes 5.
- B7 and B8 start after Q, so they come after A8 and read 5. B9 therefore writes 5.
- Every write to x after A8 is 5, and A9 comes after A8, so A9 reads 5.

**Q2: final y**
- The writes to y are A1 (5), A2 (4), B5 (6) and A6 (the value A4 read).
- A4 reads 4 if B5 is not between A2 and A4. It reads 6 if B5 is between A2 and A4.
- If A4 reads 6, A6 writes 6 and the final y is 6.
- If A4 reads 4, B5 can come after A6 (final y is 6) or before A6 (final y is 4).
- So the final y is 4 or 6.

**Q3: final z**
- The writes to z are B1 (2), B2/B3 (B3 writes 6), A3 (1) and A5 (the value A4 read).
- A5 comes after A3, and B1 comes before B3, so the final z is either A5's value or B3's 6.
- A5 writes 4 or 6, so the final z is 4 or 6.

**Pairings**
- (y=4, z=4): all of B1–B5 run first, so A2 writes 4 after B5. A4 reads 4, and A5 comes after B3.
- (y=4, z=6): A4 reads 4 and A5 writes 4. Then B3 and B5 come after A5, and A6 comes after B5.
- (y=6, z=4): A4 reads 4 and B3 comes before A5, so z ends at 4. B5 comes after A6, so y ends at 6.
- (y=6, z=6): A4 reads 6, so both A5 and A6 write 6.

BEGIN
5 4 4
5 4 6
5 6 4
5 6 6
END