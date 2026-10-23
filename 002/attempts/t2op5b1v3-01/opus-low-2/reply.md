**Answers:** A1 can return 0 or 1. The (B3, B5) pairs (1,1), (1,2), (1,3), (2,1), (2,3) and (3,1) are possible. Each pair can occur with either value of A1, giving 12 combinations.

**A1 (Q1).** A1 takes effect before A3, so A's own writes (2 and 3) cannot be visible to it. The only writes it can see are B's writes of 1.
- If A1 takes effect before B1, it returns 0.
- If A1 takes effect after B1, it returns 1.

**B3 (Q2).** B3 returns the last write before it among B1 (writes 1), A3 (writes 2) and A4 (writes 3).

**B5 (Q3).** B5 returns the last write before it among B4 (writes 1), A3 and A4. Thread A always writes 2 before 3.

**Cases by B3's value:**
- **B3 = 3.** A4 took effect before B3, so A3 did too. B4 then overwrites x with 1, so B5 = 1.
- **B3 = 2.** A3 is between B1 and B3, and A4 is after B3. A3 is already before B4, so B5 can only be 1 or 3:
  - A4 between B3 and B4, or after B5: B5 = 1.
  - A4 between B4 and B5: B5 = 3.
- **B3 = 1.** Either A3 is after B3, or both A writes are before B1.
  - A3 after B4 with A4 after B5: B5 = 2.
  - Both A3 and A4 between B4 and B5: B5 = 3.
  - Both A writes after B5, or A4 before B4: B5 = 1.

**Combining with A1.**
- A1 = 0 always works: place A1 at the very start.
- A1 = 1 needs A1 after B1 but before A3. Every case above has an execution where A3 comes after B1, so A1 = 1 also works.
- The only orderings where A1 is forced to 0 put both A writes before B1. Those give (B3, B5) = (1, 1), which other orderings already cover.

BEGIN
0 1 1
0 1 2
0 1 3
0 2 1
0 2 3
0 3 1
1 1 1
1 1 2
1 1 3
1 2 1
1 2 3
1 3 1
END