**Key constraints**

- A1 and A2 finish before P and R. A1 through A6 finish before Q and S.
- B2 and B3 come after P. B4 and B5 come after S. B6 and B7 come after R. B8 and B9 come after Q.
- A2 always reads 0 from z, because every write to z that could come first (B3, B4, B7, A6) is ordered after A2. So A3 and A7 both write 0 to x.

**Reading the values**

- **Q4 (B9):** The y-writes are A5 (value 3) and B5 (value d). A5 is before S and B5 is after S, so B5 is always the last write before B9. Therefore Q4 = Q2.
- **Q1 (A8):** Its value is 5 if B1 falls between A7 and A8, and 0 otherwise.
- **Q2 (B2):** Possible values are 0, 3, and 5. The value 3 comes from A1 being the last write before B2, which needs B1 before A1 and A3, A7 after B2.
- **Q3 (B8):** Q3 can be 0 or 5. The value 3 is impossible, because A3 (writing 0) always lands before Q and therefore before B8, overwriting A1.

**Case analysis**

- **B1 after A7:** Every A-write to x precedes B1, so Q2 = Q3 = 5. Q1 is 5 if B1 is before A8, otherwise 0.
- **B1 before A7:** Q1 = 0. The remaining combinations are:
  - A7 after B2 and before B8 gives Q2 = 5 and Q3 = 0.
  - A7 after B8 with A3 before B1 gives Q2 = 5 and Q3 = 5.
  - A3 or A7 as the last write before B2 gives Q2 = Q3 = 0.
  - A1 as the last write before B2 (B1 < A1 < B2, with A3 and A7 after B2) gives Q2 = 3 and Q3 = 0.

Each of these five combinations has a concrete interleaving that satisfies all the sync constraints. Q4 always equals Q2.

BEGIN
5 5 5 5
0 5 0 5
0 5 5 5
0 0 0 0
0 3 0 3
END