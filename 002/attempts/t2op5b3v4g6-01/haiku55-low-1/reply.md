The operations have no sync points, so the only constraints are program order within each thread and that each operation takes effect at a single instant. I enumerated the possible interleavings of the write and read instants.

**Possible values:**
- **Q1 (A2):** The last y-write before A2 is A1 (3), or B4 (1) if it falls between A1 and A2 with B5 after A2, or B5 (2) if it falls between A1 and A2.
- **Q2 (B3):** B's writes to y all come after B3, so only A's writes matter: 0 (none before B3), 3 (A1 or A4 is the last before B3), or 4 (A3 is the last before B3).
- **Q3 (final y):** A4 is always after A1 and A3, and B5 is always after B4, so the final value is 3 (A4 last) or 2 (B5 last).

**Joint feasibility:**
- **Final = 2 (A4 before B5):** B5 cannot lie between A1 and A2, so Q1 ∈ {1, 3}. Q2 = 4 forces B3 after A2, so Q1 = 3 only. That gives 1 0 2, 1 3 2, 3 0 2, 3 3 2, 3 4 2.
- **Final = 3 (B5 before A4):** Q2 = 3 via A4 would require B3 after A4, which contradicts B3 before B5, so it is infeasible. Q2 = 4 forces Q1 = 3. That gives 1 0 3, 2 0 3, 3 0 3, 1 3 3, 2 3 3, 3 3 3, 3 4 3.

Each combination has a witness interleaving; for example, 3 4 2 is A1, A2, A3, B3, A4, B4, B5, and 1 3 2 is A1, B3, B4, A2, A3, A4, B5.

Result (Q1 Q2 Q3), 12 outcomes:

BEGIN
1 0 2
1 0 3
1 3 2
1 3 3
2 0 3
2 3 3
3 0 2
3 0 3
3 3 2
3 3 3
3 4 2
3 4 3
END