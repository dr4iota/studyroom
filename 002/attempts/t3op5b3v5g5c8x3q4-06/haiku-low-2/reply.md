**Reasoning summary**

- Only the values 0 and 2 can ever be written to `x`. Value 2 comes from A3, and B4 and C5 copy values that were already read.
- A5 must read 0, but A3 always writes 2 before A5. So some 0-valued write to `x` (B4 or C5) must be the last write before A5. That rules out (Q1, Q2) = (2, 2).
- A1 must read 0 and only 0-valued or no writes can precede it, so it is satisfied by the schedules below.
- Feasible (Q1, Q2) pairs, each with a witness schedule:
  - (0, 0): e.g. C3, A1, A3, A4, B1, C5, B2, B4, A5.
  - (0, 2): forces B2 before A3 and C5, so B1 cannot come after A3 and final z cannot be 5. Witness: B1, C1, C2, B2, A1, A3, C3, A4, C5, B4, A5.
  - (2, 0): forces C3 before A3 and B4, and B2 after A3 with C5 after B2. Witnesses exist for both final z values.
- Final z: C1 always precedes C2, so 4 is impossible. Final z is 5 if B1 is the last z-write, or 1 if A4 or C2 is last. Final z = 5 requires A3 < A4 < B1 < B2, which is impossible in the (0, 2) case.

**Feasible combinations (Q1 Q2 Q3):**

- (0, 0, 1) and (0, 0, 5)
- (0, 2, 1) only
- (2, 0, 1) and (2, 0, 5)

BEGIN
0 0 1
0 0 5
0 2 1
2 0 1
2 0 5
END