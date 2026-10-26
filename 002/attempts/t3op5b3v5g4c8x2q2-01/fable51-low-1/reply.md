All answers below are reasoned from the ordering constraints.

**Q1 (C3):** The only write to z is B5. C4 (after C3) returned 0, so either B5 took effect after C4 (then C3 also sees 0) or B5 wrote 0 (then C3 sees 0 either way). So C3 = 0 always.

**Q2 (final z):** z's final value is whatever B4 read from y (or 0 if B5 wrote 0). B4 comes after B3 (writes 1), so it sees the last of B3, C1 (1), or A4. A4 writes the value A1 read from x: 0 (A1 before B2) or 5 (A1 after B2); A3 = 5 only requires A3 after B2, which is compatible with either. All three cases (1, 0, 5) are consistent with A2 = 0 and C4 = 0, since B5 can take effect after those reads (or write 0).

BEGIN
0 0
0 1
0 5
END