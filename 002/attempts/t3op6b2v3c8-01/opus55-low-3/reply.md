**Values each block can hold**

- **x:** B1 and C1 write 2. B4 writes what B2 read, and A5 writes what A3 read. Since x starts at 0, every value x ever holds is 0 or 2.
- **y:** C2 writes 1, and B3 writes what B2 read.

**What B2 can return**

B2 comes after B1, so B2 returns 2 unless a later write of 0 takes effect between B1 and B2. The only possible write of 0 is A5, and A5 writes 0 only if A3 read 0. That requires A3 to take effect before both B1 and C1. So B2 ∈ {0, 2}.

**Case B2 = 2**

- **A4:** A4 can take effect before B1 and C1 (returns 0) or after one of them (returns 2). So A4 ∈ {0, 2}.
- **B5:** B3 writes 2 to y. B5 returns 2 if C2 took effect before B3. It returns 1 if C2 took effect between B3 and B5. So B5 ∈ {1, 2}.
- **Final x:** It is 2 if B4 or C1 is the last write to x. It is 0 if A5 is last and A3 read 0.
  - A3 = 0 works with A4 = 0 (A1–A4 all take effect before B1 and C1).
  - It also works with A4 = 2 (A4 takes effect after B1 or C1).
- So all eight combinations of A4 ∈ {0, 2}, B5 ∈ {1, 2} and final x ∈ {0, 2} are possible.

**Case B2 = 0**

- This needs A3 to read 0, then B1 and C1, then A5 writing 0, all before B2.
- **Final x:** B4 then writes 0 after A5, B1 and C1 have all taken effect, so the final x is 0.
- **B5:** B3 writes 0 to y. B5 returns 0 if C2 took effect before B3, or 1 if C2 took effect between B3 and B5. So B5 ∈ {0, 1}.
- **A4:** A4 lies between A3 and A5, so it can take effect before B1 and C1 (returns 0) or after one of them (returns 2). So A4 ∈ {0, 2}.
- This adds (0 0 0) and (2 0 0). The other combinations here, (0 1 0) and (2 1 0), already appear in the first case.

BEGIN
0 1 0
0 1 2
0 2 0
0 2 2
2 1 0
2 1 2
2 2 0
2 2 2
0 0 0
2 0 0
END