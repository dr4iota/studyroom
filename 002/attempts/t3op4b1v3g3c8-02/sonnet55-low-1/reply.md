Both B2 and C2 read 0 after their own thread had already written 3. The only way a 0 can be the latest write at that point is for thread A to write 0. A2 must therefore write 0, because A1 read 0 before any 3 was written. Neither A4 nor any other write can supply that 0.

So the execution has two phases:

1. B1 and C1 (in either order), then A2 writing 0, then B2 and C2 reading 0.
2. Everything else. B3 and C3 write 2, C4 writes 3, A4 writes whatever A3 read, and A3 and B4 read.

I enumerate by the value A3 reads, which can be 0, 2 or 3.

**A3 = 0.** A4 writes 0 and can land anywhere after A3.
- B4 can be 0, 2 or 3.
- The final value can be 0 (A4 last), 3 (C4 last) or 2 (B3 last after C4).
- Final 2 requires B4 = 2. The writes after B3 are only A4 (0) and C4 (3), and C3 must precede C4, so no other 2-write can come later.
- Final 3 allows B4 = 0, 2 or 3.
- Final 0 allows B4 = 0, 2 or 3.
- This gives (0,0,0), (0,0,3), (0,2,0), (0,2,2), (0,2,3), (0,3,0), (0,3,3).

**A3 = 2.** A3 reads after B3 or C3, and A4 later writes 2. No 0 is written after A2, so B4 is 2 or 3. The final value is 2 or 3, and all four combinations are achievable.
- (2,2,2), (2,2,3), (2,3,2), (2,3,3).

**A3 = 3.** A3 reads after C4, and A4 writes 3.
- With B4 = 2, the final value is 2 if A4 precedes B3, or 3 otherwise.
- With B4 = 3, the final value must be 3, because B3 and C3 both precede B4 and nothing writes 2 afterward.
- This gives (3,2,2), (3,2,3), (3,3,3).

BEGIN
0 0 0
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 3
2 2 2
2 2 3
2 3 2
2 3 3
3 2 2
3 2 3
3 3 3
END