Key deductions:

- **Q4 (final y) is always 2.** B5 reads 2, so C3 (which writes 2) must precede B5 with no y-write between them. B3 reads 4, which forces B1 < B3 < C3 < B5, and A1 must come before B1. C3 is therefore the last y-write.
- **C2 always reads 2.** C3 is the only source of a 2 in y, and it writes the value C2 read, so C2 must have read 2. That forces C1 < C2 with neither B2 nor B4 between them.
- **Q1 (A2 reading z) is always 0.** The only write to z is C5, which comes after C3, and A2 precedes A3, which precedes C3.
- **Q2 and Q3 (x-values) depend on where B2 and B4 fall:**
  - B2 must precede C1 or follow C2, and B4 must precede C1 or follow C2.
  - If B4 < C1, all x-writes precede C1, giving C4 = 2 and final x = 2.
  - If B4 > C1 and B4 < C4, then C4 = 3 and final x = 3.
  - If B4 > C1 and C4 < B4, then C4 = 2 (it reads C1) and final x = 3.
  - If C2 < B2, then B4 is always after C1 and before C4 or after it, giving C4 = 3 and final x = 3.

Each (Q2, Q3) pair above is realized by a valid ordering of the operations.

Values in the order Q1 Q2 Q3 Q4:

BEGIN
0 3 3 2
0 2 2 2
0 2 3 2
END