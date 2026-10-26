All 12 combinations of A4 ∈ {0, 2}, B5 ∈ {0, 1, 2} and the final x ∈ {0, 2} are possible. Block x is only ever written with 0 or 2, and y is only written with B2's value or 1.

**B2.** B1 writes 2 to x before B2 runs, so B2 can read:
- 2, from B1 or C1.
- 0, if A3 read 0 before B1 and A5 then writes that 0 after B1 and before B2.

It can never read 1.

**B5.** B5 reads y after B3 has written B2's value. It returns either B2's value or 1, if C2 wrote in between.
- If B2 = 0, B5 can be 0 or 1.
- If B2 = 2, B5 can be 2 or 1.
- So B5 ∈ {0, 1, 2}, and 0 is possible only when B2 = 0.

**A4.** A4 can read 0 if it runs before any write to x. It can read 2 if it runs after B1 or C1. So A4 ∈ {0, 2}.

**Final x.**
- Final 2 is possible whenever a 2-write is last. For example, C1 or B4 comes last in the run.
- Final 0 is possible when A3 read 0 and A5 writes that 0 last. In the case B2 = 2, A5 simply runs after everything else. In the case B2 = 0, B4 writes 0 and C1 runs earlier.
- So the final x ∈ {0, 2}.

**Independence.** The three values can be chosen independently, because A4 is read between A3 and A5 and so can see 0 or 2 whatever A5 later writes. Specific schedules covering the delicate cases:
- **B2 = 2 (B5 = 1 or 2, final 0 or 2):**
  - A1–A3 read 0.
  - A4 reads 0 or 2.
  - B and C run.
  - A5 writes 0 last for final 0, or is skipped past for final 2.
- **B2 = 0, A4 = 2 (B5 = 0 or 1, final 0 or 2):**
  - A3 reads 0.
  - B1 runs.
  - A4 reads 2.
  - A5 writes 0.
  - B2 reads 0 and B3 and B4 write 0.
  - C1 runs earlier for final 0, or after B4 for final 2. For B5 = 1, C2 runs before B5; for B5 = 0, C2 runs after it.

BEGIN
0 0 0
0 0 2
0 1 0
0 1 2
0 2 0
0 2 2
2 0 0
2 0 2
2 1 0
2 1 2
2 2 0
2 2 2
END