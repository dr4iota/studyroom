Throughout, r2 is the value returned by B2. The reasoning is in three steps.

**Reads before B3.** Only A writes before B3, so B1 and B2 read the sequence 0, 1, 1, 2, 3 in order. Hence B1 ≤ r2, and r2 can be 0, 1, 2 or 3.

**B4.** B3 writes r2. The last write before B4 is either B3 or a later write by A. So B4 is r2 or a value A writes afterwards, and A's later values are never smaller than r2. The possible B4 values are:
- r2=0: 0, 1, 2 or 3
- r2=1: 1, 2 or 3
- r2=2: 2 or 3
- r2=3: 3

**Final x.** The last write is either B5, which writes r2, or A4, which writes 3. So the final value is r2 or 3.
- Final = 3 with r2 < 3 needs A4 to come after B5, hence after B4. Then B4 cannot be 3, because 3 can only come from A4 or from r2 = 3.
- Final = r2 needs A4 before B5. B4 can then take any of its values.

The combinations are as follows (B1, B4, final):
- r2=0 (B1=0): B4 any of 0–3 with final 0; B4 in {0,1,2} with final 3.
- r2=1 (B1 in {0,1}): B4 in {1,2,3} with final 1; B4 in {1,2} with final 3.
- r2=2 (B1 in {0,1,2}): B4 in {2,3} with final 2; B4 = 2 with final 3.
- r2=3 (B1 in {0,1,2,3}): B4 = 3, final 3.

BEGIN
0 0 0
0 1 0
0 2 0
0 3 0
0 0 3
0 1 3
0 2 3
1 1 1
1 2 1
1 3 1
1 1 3
1 2 3
0 2 2
0 3 2
1 2 2
1 3 2
2 2 2
2 3 2
0 2 3
1 2 3
2 2 3
0 3 3
1 3 3
2 3 3
3 3 3
0 1 1
0 2 1
0 3 1
0 1 3
END