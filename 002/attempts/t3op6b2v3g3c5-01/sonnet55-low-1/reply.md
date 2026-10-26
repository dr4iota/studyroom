Every combination below can be realised by some interleaving; the three groups follow the three possible values of A1.

**Constraints**
- B1 reads y = 0, so every write to y comes after B1.
- A3 reads 2, so the last write to x before A3 is B2, B4 or C1. A5 comes after A3, so it cannot be that write.
- A5 writes whatever A1 returned, so it writes 0, 2 or 3.
- C4 comes before C5, so it can only see y = 0 or y = 2 (from B5). It reads 2 only if B5 has taken effect.
- C2 comes after C1, so C2 can read 2 or 3. It can also read A5's value, which can be 0 if A1 read 0.

**A1 = 0**
- A1 reads before any write to x. A5 then writes 0 after A3.
- C2 = 0 occurs when A5 takes effect after C1 and before C2.
- C2 = 3 occurs when B3 is the last write before C2, for example order A1, C1, A3 (reads 2), B2, B3, C2.
- C2 = 2 is straightforward.
- C4 is 0 or 2 independently of C2, so all 6 combinations of C2 ∈ {0,2,3} and C4 ∈ {0,2} work.

**A1 = 2**
- A5 writes 2, so C2 cannot be 0.
- C2 = 3 occurs when B3 comes after C1 and before C2, with B4 after C2.
- C4 is 0 or 2, giving 4 combinations.

**A1 = 3**
- A1 reads between B3 and B4.
- A3 later reads 2 from B4 or C1.
- C2 = 3 occurs when B3 is still the last write before C2, or when A5 (writing 3) lands before C2.
- C2 = 2 is straightforward.
- C4 = 2 needs B5 after B4, which is compatible with either C2 value, giving 4 combinations.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 3 0
0 3 2
2 2 0
2 2 2
2 3 0
2 3 2
3 2 0
3 2 2
3 3 0
3 3 2
END