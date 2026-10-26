Every combination below is possible. The approach is to work out which order each operation can take effect in, then list every combination of the three values.

**When each operation can take effect**
- A1, A2, A3, B1 and B2 all finish before P.
- A4 and B3 both span P, so either can take effect first.
- B4 starts after P.

**What B1 can read (x)**
- B1 can take effect anywhere relative to A1 and A3, so it can return 0, 3 or 1.

**Q3: final y**
- A2 is the only write to y by thread A, and it happens before P.
- B4 writes y after B3, and B4 is the last write to y.
- So the final y is always the value B1 read.

**Q2: what B2 can read (y)**
- B3 cannot have taken effect yet, so B2 returns 0 or 2.
- If B1 returned 1, then A3 came before B1, so A2 did too. In that case B2 must return 2.
- If B1 returned 0 or 3, B2 can return either 0 or 2.

**Q1: what A4 can read (y)**
- A2 always takes effect before A4.
- If A4 takes effect before B3, it returns 2.
- If B3 comes before A4, and A4 comes before B4, it returns 3.
- If B4 comes before A4, it returns the value B1 read. This is possible because both take effect after P.
- When B1 read 3, this case gives 3 again, which is already counted.

**All combinations (Q1 Q2 Q3)**
- B1 = 0: A4 is 2, 3 or 0; B2 is 0 or 2; final y is 0.
- B1 = 3: A4 is 2 or 3; B2 is 0 or 2; final y is 3.
- B1 = 1: A4 is 2, 3 or 1; B2 is 2; final y is 1.

BEGIN
2 0 0
3 0 0
0 0 0
2 2 0
3 2 0
0 2 0
2 0 3
3 0 3
2 2 3
3 2 3
2 2 1
3 2 1
1 2 1
END