Only operations on y matter. B1 writes z, and B2 reads x, which no one writes, so it always returns 0.

The y-operations are:
- Thread A in order: A1 writes 3, A2 reads, A3 writes 4, A4 writes 3.
- Thread B in order: B3 reads, B4 writes 1, B5 writes 2.

**B3 (Q2).** B3 comes before B4 and B5, so it sees only A's writes (or nothing):
- 0 if it is before A1.
- 3 if it is after A1 and before A3, or after A4.
- 4 if it is between A3 and A4.

**A2 (Q1).** A2 is after A1, so it returns the last write before it among A1 (3), B4 (1) and B5 (2):
- 3 if neither B4 nor B5 falls between A1 and A2.
- 1 if B4 falls between A1 and A2 and B5 does not.
- 2 if B5 falls between A1 and A2.

**Final y (Q3).** The last write overall decides it:
- 3 if A4 comes after B5.
- 2 if B5 is last.

**Combinations**
- B3 = 0 (before A1):
  - A2 = 3, final 3 or 2. Final 3 comes from B3, B4, B5 all before A1, or from B5 between A2 and A4. Final 2 comes from B5 after A4.
  - A2 = 1, final 3 or 2. B4 falls between A1 and A2, and B5 falls after A2, either before or after A4.
  - A2 = 2, final 3 only. B5 falls before A2, so A4 is later.
- B3 = 3 (after A1, before A3): B4 and B5 must come after B3, and the same A2 analysis gives:
  - A2 = 3, final 3 or 2.
  - A2 = 1, final 3 or 2.
  - A2 = 2, final 3 only.
- B3 = 4 (between A3 and A4): B4 and B5 are after A3, so A2 = 3. Final is 3 if B5 is before A4, or 2 otherwise.
- B3 = 3 (after A4): A2 = 3 and B5 is last, so final is 2. This is already covered above.

BEGIN
3 0 3
3 0 2
1 0 3
1 0 2
2 0 3
3 3 3
3 3 2
1 3 3
1 3 2
2 3 3
3 4 3
3 4 2
END