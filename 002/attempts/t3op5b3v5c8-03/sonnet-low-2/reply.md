Every combination below is checked against the three threads' program orders; each thread's operations can interleave in any way.

**Fixed facts**
- Nothing ever writes a nonzero value to z, so A3 reads 0. A4 therefore writes 0 to y and A5 writes 0 to z.
- The writes to y are A1 (3), A4 (0), B2 (5) and C1 (2). A4 always comes after A1.
- B1 comes before B2, so B1 cannot return 5. B1 can return 0 (the initial value, or A4's write), 2 (C1) or 3 (A1).
- B4 comes after B2, so B4 can return 5, 3, 2 or 0.
- The final value of y cannot be 3, because A4 overwrites A1. It can be 0, 2 or 5.

**Final y = 5.** B2 is the last write, so B4 returns 5. B1 can be 0, 2 or 3. This gives (0,5,5), (2,5,5), (3,5,5).

**Final y = 0.** A4 is the last write.
- B4 can be 5, 3, 2 or 0, and B1 can be 0, 2 or 3.
- B1=3 with B4=3 is impossible: A1 is the only write of 3 and B2 sits between B1 and B4.
- B1=2 with B4=2 is impossible for the same reason with C1.
- That leaves 12 − 2 = 10 combinations.

**Final y = 2.** C1 is the last write, so B1 cannot return 2.
- B1 can be 0 or 3.
- B4 can be 5, 2 or 0 with either B1 value, which gives 6 combinations.
- B4=3 needs A1 after B2, so B1 cannot be 3. That adds only (0,3,2).
- This gives 7 combinations.

BEGIN
0 5 5
2 5 5
3 5 5
0 5 0
0 3 0
0 2 0
0 0 0
2 5 0
2 3 0
2 0 0
3 5 0
3 2 0
3 0 0
0 5 2
3 5 2
0 3 2
0 2 2
3 2 2
0 0 2
3 0 2
END