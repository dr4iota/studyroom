**Answer:** B6 and B7 can return any of 0, 1, 2 or 3 in the combinations listed below, and the final y is 0 or 1. A combination where B6 or B7 returns 1 is only possible with final y = 0.

**Fixed timing.**
- All of thread B ends by P, because B7 ends at P.
- A1 is before P, and A2 spans P.
- A3 and A4 are before Q. A5 and A6 are after R.
- C5 ends after Q, and C1 through C6 are before R. So C6 is before R, which is before A5.

**What x can hold.**
- B3 runs after B2, which writes x = 1. The only other write to x, A3, comes after P, so B3 returns 1. B4 then writes 1.
- A1 and C1 each return 0 if they run before B2, and 1 if they run after it.

**Final y.**
- A5 is the only write to y after R, so final y equals the value read by A1.

**C7 returns 0.**
- C7 runs after C6, so the last write to y before C7 is either C6 or A5.
- If it is C6, then C1 = 0.
- If it is A5, then A1 = 0.
- So (A1, C1) can be (1, 0), (0, 0) or (0, 1), but not (1, 1).
- If A1 = 1, then C1 = 0, which forces C1 before B2 and A1 after B2. That is possible.
- A2 can return 3 by having C3 or C5 take effect just before it.

**What B6 and B7 can see.**
- After B5 writes 2, only thread C writes to y before P. Thread C's writes come in this order: C2 writes the value read by C1, then C3 and C5 write 3.
- So y moves through 2, then C1's value, then 3. C2 may also come before B5, in which case y goes straight from 2 to 3.
- B6 and B7 read in order, so the possible pairs are: (2,2), (2,c), (2,3), (c,c), (c,3) and (3,3), where c is C1's value.

**Combining the cases.**
- When C1 = 0, the pairs are (2,2), (2,0), (2,3), (0,0), (0,3) and (3,3). Final y can be 0 or 1.
- When C1 = 1, the pairs are (2,2), (2,1), (2,3), (1,1), (1,3) and (3,3). Final y is 0, because A1 must be 0.

BEGIN
2 2 0
2 2 1
2 0 0
2 0 1
2 3 0
2 3 1
0 0 0
0 0 1
0 3 0
0 3 1
3 3 0
3 3 1
2 1 0
1 1 0
1 3 0
END