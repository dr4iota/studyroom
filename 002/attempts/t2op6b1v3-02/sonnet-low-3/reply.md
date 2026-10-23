Neither thread has a sync point, so every interleaving that keeps each thread's own order is allowed.

**Q1 (B1).** B's own writes come after B1, so B1 can't return 1. Thread A writes 2, then 3, then 2, so B1 can return 0, 2 or 3.

**Q2 (B4).** B4 comes after B3, so it can return 1 (B3's write, with no A write in between). It can also return 2 or 3 if A writes land between B3 and B4, so B4 ∈ {1, 2, 3}.

**Q3 (final x).** A5 is the last write of A and B5 is the last write of B, so the final value is whichever of them takes effect last. That gives 2 or 1. It can't be 3, because A5 always comes after A4.

**Combinations.** I checked each B1 value against each B4 value and each final value, and every combination can be realised:
- B1=0: B1 happens before A3. For any B4 and any final value, place the A writes around B3, B4 and B5 as needed.
- B1=2: A3 has happened and A4 has not (or A5 has finished). B4=3 needs A4 between B3 and B4. B4=2 comes from A3 or A5. A final value of 2 needs A5 after B5.
- B1=3: A4 has happened. B4=2 needs A5 between B3 and B4. B4=3 needs A5 after B4. A final value of 2 needs A5 after B5, and a final value of 1 needs B5 after A5.

That gives 3 × 3 × 2 = 18 combinations.

BEGIN
0 1 1
0 1 2
0 2 1
0 2 2
0 3 1
0 3 2
2 1 1
2 1 2
2 2 1
2 2 2
2 3 1
2 3 2
3 1 1
3 1 2
3 2 1
3 2 2
3 3 1
3 3 2
END