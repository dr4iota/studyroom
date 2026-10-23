The only possible pairs (A5, B3) are 3 0, 3 1, 3 2, 3 3, 0 0, 0 1, 0 2, 0 3, 2 1, 2 2, 2 3, 1 1 and 1 3.

**Setup**
- Thread A writes 2, 3, 1, 3 to x in that order, then reads x in A5.
- Thread B reads x three times (B1, B2, B3). Call the value B2 returns v. B4 and B5 both write v.
- Before B4 takes effect, only A writes x. Over time, x holds 0, then 2, 3, 1, 3.

**What A5 can return**
- A5 returns 3 if neither B4 nor B5 takes effect between A4 and A5.
- Otherwise A5 returns v, because whichever B write lands last before A5 writes v.

**What B3 can return**
- B3 comes after B2 and before B4, so it sees x only as A has left it.
- It must read a value at the same point in A's sequence as B2 or later.

**Case 1: A5 = 3**
- Let B4 and B5 take effect after A5.
- B3 can then read any of 0, 2, 3, 1 by placing B2 and B3 suitably.
- Pairs: (3,0), (3,2), (3,3), (3,1).

**Case 2: A5 = v (B4 or B5 takes effect between A4 and A5)**
In each sub-case, B4 can be placed after A4, so B3 is free to land anywhere after B2.
- **v = 0** (B2 reads before A1): B3 can read 0, 2, 3 or 1. Pairs: (0,0), (0,2), (0,3), (0,1).
- **v = 2** (B2 reads after A1, before A2): B3 can read 2, 3 or 1. Pairs: (2,2), (2,3), (2,1).
- **v = 3**: these pairs are already covered in Case 1.
- **v = 1** (B2 reads after A3, before A4): B3 can read 1 or 3. Pairs: (1,1), (1,3).

BEGIN
3 0
3 1
3 2
3 3
0 0
0 1
0 2
0 3
2 1
2 2
2 3
1 1
1 3
END