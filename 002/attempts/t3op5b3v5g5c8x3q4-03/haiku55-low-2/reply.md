**Key constraints**

- The y-writes are C1 (writes 2) and B4 (writes B1's value). The only other value in play is 0, so B1 must read 2, which requires C1 before B1.
- B5 reads z=2, so the last z-write before B5 must be B3, which writes 2. That forces C1 < B1 < B3 < B5.
- A2 reads y=2, which requires C1 before A2.
- C2 reads z=3, so A1 is the last z-write before C2.

**Asked values**

- **Q1 (B2):** B2 follows B1, which follows C1, so y is already 2 and B2 returns 2 in every execution.
- **Q2 (C4):** C4 returns 5 (from C3) or 2 (from A3, if A3 lands between C3 and C4). Both are reachable.
- **Q3 (final y):** Every write to y stores 2, so the final y is always 2.
- **Q4 (final z):** A4 always comes after A1 in program order, so 3 is impossible. The final z can be 4 (A4 last) or 2 (B3 last, with A4 before B3). Both are reachable.

**Witness schedules (oldest first)**

- Q2=2, Q4=4: A1, C1, B1, B2, C2, B3, C3, A2, A3, C4, B4, B5, A4
- Q2=5, Q4=4: A1, C1, B1, B2, C2, B3, C3, C4, A2, A3, B4, B5, A4
- Q2=2, Q4=2: A1, C1, B1, B2, C2, C3, A2, A3, C4, A4, B3, B4, B5
- Q2=5, Q4=2: A1, C1, B1, B2, C2, C3, C4, A2, A3, A4, B3, B4, B5

Each of the four combinations is achievable, and no other combinations are possible.

BEGIN
2 2 2 2
2 2 2 4
2 5 2 2
2 5 2 4
END