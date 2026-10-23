Each combination below is shown with a witnessing order of operations.

**Forced facts:**
- Only B1 writes x (value 3), so x is 0 before B1 and 3 after. C1 (reads 0) is before B1. C2, C4 and A3 (read 3) are after B1.
- B3 comes after B1 in thread B, so B3 reads 3 and B4 writes 3 to y.
- C3 is before C5 in thread C, so C5 always happens after C3.
- z is written by A1 (1), B2 (1), and A4 (the value A2 read).

**Reasoning for Q1 (value of C3):**
- **0:** C3 happens before A1 and B2 (after B1). Example order: C1, B1, C2, C3, C4, C5, B2, B3, B4, then the A operations.
- **1:** B2 or A1 happens before C3, and A4 happens after C3. Example order: C1, B1, B2, C2, C3, C4, C5, B3, B4, then the A operations.
- **3:** Only A4 can write 3, so A4 happens before C3 with A2 reading 3. That forces A2 before C3 before C5, and the only way A2 reads 3 is B4 before A2 before C5. So B4 precedes C5 and the final y is 4. Example order: C1, B1, C2, B2, B3, B4, A1, A2, A3, A4, C3, C4, C5.
- **4:** Only A4 can write 4, which needs A2 to read 4. That requires C5 before A2, but A2 is before C3, which is before C5. Impossible.

**Reasoning for Q2 (final y):**
- Final y is 4 if C5 is after B4, and 3 if B4 is after C5.
- Both orders are possible for value 0 and value 1 (examples above). For value 3, only final y = 4 is possible, as shown.

**Feasible (Q1, Q2) pairs:** (0,3), (0,4), (1,3), (1,4), (3,4).

BEGIN
0 3
0 4
1 3
1 4
3 4
END