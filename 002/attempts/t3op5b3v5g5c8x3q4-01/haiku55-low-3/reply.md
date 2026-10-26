The possible outcomes are `(Q1, Q2, Q3) = (0,3,0), (1,3,1), (2,3,2), (3,3,3)`.

**Key constraints**

- **y:** Only B2 writes y, with value 3. A3 reads 3, so B2 must precede A3. The final y is always 3, so Q2 = 3.
- **z:** C2 reads 3, and the only writes to z that can precede C2 are C1 (4) and B3 (3). So C1 < B3 < C2 < C3 < C5 in time. C5 is therefore the last write to z, and its value is C4's result. So Q3 = Q1.
- **x:** The writes are A1 (2), A4 (the value A2 read, which is 0 or 3), and B5 (1). B1 reads 0, so B1 must precede A1 and any nonzero write to x.

**Possible values of C4 (Q1)**

- **0:** Order B1 B2 C1 B3 C2 C3 C4 A1 A2 A3 A4 B4 B5 C5. C4 sees no x write.
- **1:** Order B1 B2 C1 B3 C2 C3 A1 A2 A3 A4 B4 B5 C4 C5. B5 is the last x write before C4.
- **2:** Order B1 B2 C1 B3 C2 C3 A1 A2 A3 C4 A4 B4 B5 C5. A1 is the last x write before C4.
- **3:** Order B1 B2 A1 A2 C1 B3 C2 C3 A3 A4 C4 B4 B5 C5. A2 reads 3 (B2 precedes it), A4 writes 3, and that is the last x write before C4.

No other value is possible, since x only ever holds 0, 1, 2, or 3.

BEGIN
0 3 0
1 3 1
2 3 2
3 3 3
END