Every outcome below is achievable by some interleaving, and all other combinations are impossible.

**Q1 (B1).** B1 runs before B3, so B1 can only see 0 or one of A's values. It cannot see 1. So B1 is 0, 2 or 3.

**Final value of x.** A4 (the write of 3) is always followed by A5 (the write of 2). So the last write overall is either A5 (2) or B5 (1), and 3 is never final.

**B4.** B4 follows B3, so it reads 1 or a later A write (2 or 3).

**Case B1 = 0.** B1 comes before A3, so no constraint ties A's writes to B3 and B4. B4 can be 1, 2 or 3, and the final value can be 1 or 2 in each case. That gives all 6 combinations.

**Case B1 = 2.** A3 is before B1, and A4 is after B1.
- B4 = 1 works with final 1 or 2.
- B4 = 3 works with final 1 or 2. A4 falls between B3 and B4, and A5 goes either after B5 (final 2) or before B5 (final 1).
- B4 = 2 requires A5 to land between B3 and B4, because A3 is already overwritten by B3. Then A5 is before B5, so the final value is 1 only.

That gives 5 combinations.

**Case B1 = 3.** A4 is before B1, and A5 is after B1. B3 therefore comes after A4, so B4 cannot be 3.
- B4 = 1 works with final 1 or 2.
- B4 = 2 requires A5 before B4, so the final value is 1 only.

That gives 3 combinations.

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
2 3 1
2 3 2
3 1 1
3 1 2
3 2 1
END