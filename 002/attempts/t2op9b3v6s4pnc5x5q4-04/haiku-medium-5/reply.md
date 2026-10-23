I worked this out by hand by reducing the constraints to ordering rules between the operations, then checking each candidate outcome against a concrete schedule.

**Key observations**

- **Final z:** B8 (`z := value of B2`) is always the last write to z. It comes after A9, which comes after all of A's z-writes, and after B1. So final z = Q1 = Q4 = value read by B2.
- **Final y:** A8 is the only write to y, and it always happens. So final y = value read by A7 = value read by A4 (since A6 writes that value to z just before A7).
- **Value read by A4:** B1 must precede A3, hence A4. So A4 reads 1 if A1 < B1, and 6 if B1 < A1.
- **Value read by B2:** y is 0 unless A8 precedes B2, in which case it is the value of A8's write.
- **Final x:** B7 always overwrites B5 and B6. Final x is 1 only if A2 comes after B7, otherwise 4.
- **Infeasible pairing:** If B2 reads a nonzero y, then A8 < B2 < B7, so B7 precedes A2 is impossible (A2 < A8). So Q2 = 1 is impossible when Q1 ≠ 0.

**Feasible outcomes (each checked with a concrete schedule)**

- Q3 = 1, Q1 = 0: Q2 = 1 (order A1, B1, B2…B6, B7, A2, …) and Q2 = 4 (order A1, B1, B2…B6, A2, B7, …).
- Q3 = 1, Q1 = 1: Q2 = 4 only (order A1, B1, A2…A8, B2…B7, A9, B8, B9).
- Q3 = 6, Q1 = 0: Q2 = 1 and Q2 = 4 (B1 first, then A1, with B2 before A8).
- Q3 = 6, Q1 = 6: Q2 = 4 only (order B1, A1, A2…A8, B2…B7, A9, B8, B9).

BEGIN
0 1 1 0
0 4 1 0
1 4 1 1
0 1 6 0
0 4 6 0
6 4 6 6
END