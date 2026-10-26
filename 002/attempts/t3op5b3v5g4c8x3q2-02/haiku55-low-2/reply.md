The possible (Q1, Q2) pairs are 0 0, 3 0, 1 1, 3 1, 2 2, and 3 2.

**Key facts**

- **y:** Writes A1 (y=1) then A2 (y=2). C2 reads 1, so A1 < C2 < A2. C5 reads 2, so A2 < C5.
- **x before A3:** C1 (x=3) precedes C2, which precedes A2, which precedes A3. So C1 always happens before A3, and the value A3 reads is either 3 (if C1 is the last x-write before A3) or the value B4 wrote, which is B3's value Q2 (if B4 falls between C1 and A3). So Q1 ∈ {3, Q2}.
- **z:** B5 must see 1. This is always achievable by placing C3 and C4 before B5 and A4 and A5 after B5, so it does not restrict the other values.

**Cases by Q2 (the value B3 reads from y)**

- **Q2 = 0** (B3 before A1): Q1 = 0 needs C1 < B4 < A3, e.g. C1, B1, B2, B3, B4, A1, C2, A2, A3. Q1 = 3 needs B4 before C1, e.g. B1–B4, C1, A1, C2, A2, A3.
- **Q2 = 1** (A1 < B3 < A2): Q1 = 1 needs C1 < B4 < A3, e.g. C1, A1, B1, B2, B3, B4, C2, A2, A3. Q1 = 3 needs C1 after B4, e.g. A1, B1, B2, B3, B4, C1, C2, A2, A3.
- **Q2 = 2** (B3 after A2): Q1 = 2 needs C1 < B4 < A3 and B4 before A3, e.g. C1, A1, C2, A2, B1, B2, B3, B4, A3. Q1 = 3 needs A3 before B4, e.g. C1, A1, C2, A2, A3, B1, B2, B3, B4.

BEGIN
0 0
3 0
1 1
3 1
2 2
3 2
END