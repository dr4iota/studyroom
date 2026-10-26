Q1 is the value B2 returns and Q2 is the final value of x. Ten combinations are possible.

**Key facts:**
- B2 always follows B1 (which writes 2), so B2 can never read 0.
- A final value of 1 from C4 alone is impossible. If C4 were the last write, B3 would need A3 to have written 1 before it, but A1 would then need to read 1 from C4, which is after A1. This is a contradiction.
- So the final value is whatever A3 or B4 wrote last. When A1 reads 1, B3 forces A3 to sit before B3 and B4 to come after it, so the final value equals b2.

**Witness schedules (abbreviated):**
- (1,0): A1(0), B1, A2, C1–C4, B2(1), B3, B4(1), A3(0)
- (1,1): A1(0), B1, A2, C1–C4, B2(1), B3, A3(0), B4(1)
- (1,2): B1, A1(2), A2, C1–C4, B2(1), B3, B4(1), A3(2)
- (1,3): C1, C2, A1(3), C3, A2, B1, C4, B2(1), B3, A3(3), B4(1)
- (2,0): A1(0), B1, B2(2), A2, C1–C4, B3, B4(2), A3(0)
- (2,2): B1, A1(2), A2, B2(2), C1–C4, B3, A3(2), B4(2)
- (2,3): C1, C2, A1(3), C3, A2, B1, B2(2), C4, B3, B4(2), A3(3)
- (3,0): A1(0), B1, A2, C1, C2, B2(3), C3, C4, B3, B4(3), A3(0)
- (3,2): B1, C1, C2, B2(3), C3, A1(2), A2, A3(2)... with C4, B3, B4(3), then A3(2) last
- (3,3): B1, C1, C2, B2(3), A1(3), C3, A2, C4, B3, B4(3), A3(3)

BEGIN
1 0
1 1
1 2
1 3
2 0
2 2
2 3
3 0
3 2
3 3
END