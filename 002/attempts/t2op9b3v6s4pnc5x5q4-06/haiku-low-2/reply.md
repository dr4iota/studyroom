**Key deductions**

- **A4 always reads 0.** Thread A's A1–A5 all take effect before S, and B1 takes effect after S. Every write to y (B4, B7) comes after B1, so y is still 0 when A4 reads it.
- **B1 always reads 0.** No write to y occurs before B1 in any execution.
- **A6 writes 0 to z and A8 writes 0 to x.**
- **Q1 is always 0.** A8 (writes 0 to x) precedes A9 in program order, so A9 reads 0.
- **B5 and B8 read either 4 or 0.** Both come after B2 (writes 4 to x). The value is 0 only if A8 lands between B2 and the read, and 4 otherwise.
- **Q3 (final x) equals rB5.** A8 precedes A9, which precedes P, which precedes B9, so B9 is the last write to x and writes the value B5 read.
- **Q4 (final z) is 0 or 1.** B3 always precedes B6, and A5 always precedes A6, so the last write to z is either A6 (value 0) or B6 (value 1). A6 is forced before B6 whenever A8 is before B5, because A6 precedes A8 in program order.

**Placements of A8 relative to B2, B5, B8**

| Case | A8 position | rB5 (Q3) | rB8 (Q2) | Final z (Q4) |
|---|---|---|---|---|
| a | before B2 | 4 | 4 | 1 only |
| b | between B2 and B5 | 0 | 0 | 1 only |
| c | between B5 and B8 | 4 | 0 | 0 or 1 |
| d | after B8 | 4 | 4 | 0 or 1 |

Each placement is consistent with the sync constraints (S < B1 < R < A8 < A9 < P < B9, and B4 < Q < A9), so all cases are feasible.

**Distinct combinations (Q1 Q2 Q3 Q4)**

BEGIN
0 0 0 1
0 0 4 0
0 0 4 1
0 4 4 0
0 4 4 1
END