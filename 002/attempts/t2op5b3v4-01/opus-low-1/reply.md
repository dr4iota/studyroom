**Approach.** Thread A reads z once (A1), then writes 3, 4, 2 to z in that order. Thread B writes 3 and then 2 to z, reads z (B4), and finally writes 1 to z. The reads of x (A2) and the write to y (B2) cannot change any of the three asked values. So only the order of the z operations matters.

**Q1, the value A1 returns.** A1 runs before all of A's writes. It therefore sees either the initial 0 or the latest of B's writes that took effect before it.
- 0: A1 takes effect before B1.
- 3: A1 takes effect after B1 and before B3.
- 2: A1 takes effect after B3 and before B5.
- 1: A1 takes effect after B5.

**Q2, the value B4 returns.** B4 comes after B3, so it sees B3's 2 or a later write by A.
- 2: no A write falls between B3 and B4, or A5 is the last write before B4.
- 3: A3 falls after B3 and is the last write before B4, with A4 after B4.
- 4: A4 is the last write before B4, with A5 after B4.

**Q3, the final value of z.** The last write is either A5 (giving 2) or B5 (giving 1).

**Combining the cases.**
- **A1 = 0, 3 or 2.** A1 takes effect before B5, and all of A's writes come after A1. A's writes can still fall anywhere around B3, B4 and B5, so every Q2 value can occur with every final value:
  - B4 = 2 via B3, then A5 after B5: final 2.
  - B4 = 2 via A5 before B4: final 1.
  - B4 = 3 or 4, then A5 before or after B5: final 1 or 2.
  
  That gives all 6 pairs for each of these three A1 values.
- **A1 = 1.** A1 is after B5, so all of A's writes come after B4 and B5. B4 must return 2, and A5 is the last write, so z ends at 2. That gives only one combination.

This gives 3 × 6 + 1 = 19 combinations.

BEGIN
0 2 1
0 2 2
0 3 1
0 3 2
0 4 1
0 4 2
3 2 1
3 2 2
3 3 1
3 3 2
3 4 1
3 4 2
2 2 1
2 2 2
2 3 1
2 3 2
2 4 1
2 4 2
1 2 2
END