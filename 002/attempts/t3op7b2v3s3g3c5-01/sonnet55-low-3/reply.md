Every combination of (B6, B7) from the list below is possible, and the final y can be 0 or 1 independently of them.

**Constraints on the timeline**
- All of B ends before P. A2 starts before P and ends after P, and A2 ends before Q.
- A3 and A4 come after Q. C5 ends after Q. C6 ends before R. A5 and A6 come after R.
- Because C5 ends after Q, C5 takes effect after every B operation. The only writes to y that can happen during B's operations are B1 (3), B5 (2), C2 (the value C1 read) and C3 (3).

**Values of x**
- Before A3, only B2 (1) and B4 can write x, and B4 writes what B3 read. B3 reads 1, so B4 also writes 1.
- A1 therefore reads 0 or 1. Call that value a.
- C7 returned 0, and C5 wrote 3 earlier. So the last write to y before C7 must be C6, and it must write 0. That forces C1 to read 0, which means C1 takes effect before B2.

**Q1 and Q2 (B6 and B7)**
- B6 and B7 come after B5, so y starts at 2 for them.
- C2 (writing 0) and then C3 (writing 3) can land between B5 and the reads, in that order. So y can pass through 2, then 0, then 3.
- B6 and B7 are consecutive reads, so each can only see the same or a later stage of that sequence.
- The possible pairs are (2,2), (2,0), (2,3), (0,0), (0,3) and (3,3).
- The pairs (3,0), (3,2) and (0,2) are impossible because they need y to go backwards through that sequence.
- Each pair is consistent with A2 reading 3. A2 can take effect right after B1 and before B5, when y is 3.

**Q3 (final y)**
- After C6, the remaining writes to y are A4 (3) and then A5 (the value a). C7 is only a read.
- A5 comes after A4, so the final y is a.
- Both a=0 and a=1 are achievable. a=1 requires A1 to read after B2, and C1 still reads before B2.
- C7 still returns 0 in both cases. A4 happens before C6, and A5 happens either after C7 or writes 0.

BEGIN
2 2 0
2 2 1
2 0 0
2 0 1
2 3 0
2 3 1
0 0 0
0 0 1
0 3 0
0 3 1
3 3 0
3 3 1
END