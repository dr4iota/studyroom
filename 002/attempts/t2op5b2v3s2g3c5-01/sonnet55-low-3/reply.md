Reading the sync points: B1–B4 finish before Q and A5 starts after Q, so B1–B4 all take effect before A5. A1–A5 all finish before P. B5 starts before P and ends after P, so its write can take effect before or after A4's write.

**Q1 (A1 reads y).** A1 runs before A4, so it can't see 2. It can read 0, 1 (from B1) or 3 (from B2). Call this value a.

**Q2 (B3 reads y).** B2 writes 3 before B3, so B3 returns 3 unless something overwrites it first. The only possible overwrites are A2 (writes a) and A4 (writes 2). So B3 ∈ {3, a, 2}.

**Q3 (final y).** The last write to y is either A4's 2 or B5's 1.
- Final 2 means A4 takes effect after B5. B5 is after B3, so A4 is after B3, and B3 can't read 2.
- Final 1 means B5 takes effect after A4. A4 can then fall before B3, so B3 can read 2.

Combinations (a, b, final y):
- a=0: b=0, 3 with final 1 or 2; b=2 with final 1 only.
- a=1: b=1, 3 with final 1 or 2; b=2 with final 1 only.
- a=3: b=3 with final 1 or 2; b=2 with final 1 only.

Each combination is achievable with an explicit interleaving. For example, A1 reads 0, then B1, B2, A2 writes 0, A3, A4 writes 2, B3 reads 2, B4, then B5 gives (0, 2, 1).

BEGIN
0 0 1
0 0 2
0 2 1
0 3 1
0 3 2
1 1 1
1 1 2
1 2 1
1 3 1
1 3 2
3 2 1
3 3 1
3 3 2
END