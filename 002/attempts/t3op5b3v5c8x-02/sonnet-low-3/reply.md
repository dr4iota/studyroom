Each triple below is C3, C4 and the final value of y. I worked these out by hand by enumerating the possible orders of the writes to y; I did not run a program to check them.

**Writes to y.** The writes to y are A1 (4), C2 (1), B3 (5) and B5. B5 writes whatever B1 read, which can be 0, 4 or 1; it cannot be 5, because B3 comes after B1. B3 always precedes B5, so B3 can never be the last write. The final value of y is therefore 0, 1 or 4.

**Reads.** C3 and C4 both happen after C2. They see the history of y from C2 onward, and C4 never sees an earlier point in that history than C3.

**Final y = 0.** B5 writes 0 last, so B1 read 0 and ran before A1 and C2. A1, C2 and B3 fall between B1 and B5 in any order. The possible (C3, C4) pairs are:
- (1,1), (1,4), (1,5), (1,0)
- (4,4), (4,5), (4,0)
- (5,5), (5,4), (5,0)
- (0,0)

**Final y = 1.** Either C2 is the last write, or B5 writes 1 last.
- If B5 writes 1 last, B1 read 1, and A1 comes either before C2 or after B1.
- The possible pairs are (1,1), (1,4), (1,5), (4,1), (4,4), (4,5), (5,1), (5,4), (5,5).

**Final y = 4.** Either A1 is the last write, or B5 writes 4 last after B1 read 4.
- The possible pairs are (0,0), (0,4), (1,0), (1,1), (1,4), (1,5), (4,4), (4,5), (5,0), (5,1), (5,4), (5,5).
- (4,1) is impossible with final y = 4. A 4 followed by a 1 requires B5 to write 1 after A1, which leaves the final value at 1.
- (0,1) and (0,5) are impossible with final y = 4. A 0 can only come from B5, which comes after C2 and B3, so neither a 1 nor a 5 can follow it.

BEGIN
0 0 0
1 0 0
1 1 0
1 4 0
1 5 0
4 0 0
4 4 0
4 5 0
5 0 0
5 4 0
5 5 0
1 1 1
1 4 1
1 5 1
4 1 1
4 4 1
4 5 1
5 1 1
5 4 1
5 5 1
0 0 4
0 4 4
1 0 4
1 1 4
1 4 4
1 5 4
4 4 4
4 5 4
5 0 4
5 1 4
5 4 4
5 5 4
END