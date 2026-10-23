The 12 possible (Q1, Q2) pairs are below, where Q1 is the value returned by B2 and Q2 is the final value of x.

**Key facts from the constraints:**
- The final value is the last write overall, so it must come from B4 (writes Q1), A3 (writes A1's value), or C4 (writes 1). C4 can never be last, because B3 reads 1 and must see a source that comes before B4.
- B3 reads 1, so its source is either C4 (which must come before B3) or A3 with A1 = 1.
- A2 reads 2, so the last write before A2 must be 2 (from B1, C1, C3, or B4 with value 2).

**Witness schedules (one per pair):**
- (0,0): A1, B1, C1, A2, C2, C3, A3(0), B2, C4, B3, B4(0) (A1 reads 0, and A3 writes 0 before B2 so B2 reads 0)
- (1,1): A1(0), B1, C1, A2, C2, C3, C4, B2(1), B3(1), A3(0), B4(1)
- (2,2): A1(0), B1, B2(2), C1, A2, C2, C3, C4, B3(1), A3(0), B4(2)
- (3,3): A1(0), B1, C1, A2, C2, B2(3), C3, C4, B3(1), A3(0), B4(3)
- (1,0): A1(0), B1, C1, A2, C2, C3, C4, B2(1), B3(1), B4(1), A3(0)
- (2,0): A1(0), C1, B1, B2(2), A2, C2, C3, C4, B3(1), B4(2), A3(0)
- (3,0): A1(0), C1, B1, A2, C2, B2(3), C3, C4, B3(1), B4(3), A3(0)
- (1,2): C1, A1(2), B1, A2, C2, C3, C4, B2(1), B3(1), B4(1), A3(2)
- (3,2): C1, A1(2), B1, A2, C2, B2(3), C3, C4, B3(1), B4(3), A3(2)
- (1,3): C1, B1, C2, A1(3), C3, A2, C4, B2(1), B3(1), B4(1), A3(3)
- (2,3): C1, B1, C2, A1(3), C3, B2(2), A2, C4, B3(1), B4(2), A3(3)
- (2,1): C1, B1, B2(2), C2, C3, C4, A1(1), B3(1), B4(2), A2, A3(1)

**Impossible pairs:** (3,1) cannot occur, since reading 3 in B2 and ending with 1 would require A1 = 1 alongside B2 = 3, and A2 then has no source for 2. Q2 = 3 with Q1 = 0 cannot occur either, since B2 = 0 requires A3 to write 0 before B2, which makes A3 non-last. Q2 = 0 with Q1 ≠ 0 is achievable, as shown above.

BEGIN
0 0
1 0
1 1
1 2
1 3
2 0
2 1
2 2
2 3
3 0
3 2
3 3
END