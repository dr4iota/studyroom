All six combinations of A3 and A4 are possible, and each can end with x = 2 or x = 4.

**Constraints on x**
- A1 reads 0 and B2 reads 2, so A1 takes effect before B1, and B1 before B2.
- A5 must not take effect between B1 and B2, or B2 would read 4. So A5 comes either before B1 or after B2.
- B5 writes 2 after B4, and A5 writes 4 after A4. The final value of x is whichever of A5 and B5 takes effect last.

**Constraints on y**
- y is written only by B3 (1) and then B4 (3), so it goes 0, then 1, then 3.
- A3 and A4 read y in order, so the pair (A3, A4) never decreases. The possible pairs are (0,0), (0,1), (0,3), (1,1), (1,3) and (3,3).
- A5 can be placed before B1 only if A3 and A4 have already read, which forces both to read 0. In every other case A5 is after B2 anyway.

**Final value of x for each pair**
- (0,0): A5 can come before B1, so B5 is last and x = 2. A5 can also come after B5, so x = 4. Both are possible.
- (0,1): A4 reads between B3 and B4. A5 can be before or after B5, so both 2 and 4 are possible.
- (1,1): A4 reads before B4, so the same freedom applies. Both are possible.
- (0,3), (1,3), (3,3): A4 reads after B4, and A5 can still be before or after B5. Both are possible.

BEGIN
0 0 2
0 0 4
0 1 2
0 1 4
0 3 2
0 3 4
1 1 2
1 1 4
1 3 2
1 3 4
3 3 2
3 3 4
END