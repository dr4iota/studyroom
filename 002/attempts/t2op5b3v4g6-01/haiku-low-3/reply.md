The writes to y that matter are A1 (3), A3 (4), A4 (3), B4 (1), and B5 (2). B1 and B2 don't touch y, and x is always 0. With no sync points, the only constraints are the order within each thread, so the possible executions are all interleavings of A1<A2<A3<A4 with B3<B4<B5.

Each interleaving can be described by how many A-operations precede B3, B4, and B5. Call these counts a ≤ b ≤ c, each between 0 and 4. From these:

- **Q1 (A2):** A2 reads 2 if c = 1, reads 1 if b = 1 and c ≥ 2, and otherwise reads 3 (from A1).
- **Q2 (B3):** B3 reads 0 if a = 0, 3 if a = 1 or 2, 4 if a = 3, and 3 if a = 4.
- **Q3 (final y):** The last write is B5 if c = 4 (value 2), and A4 otherwise (value 3).

Checking which triples are achievable gives 12 distinct combinations. For example, (1 0 2) comes from the order B3, A1, B4, A2, A3, A4, B5, and (3 4 3) from A1, A2, A3, B3, B4, B5, A4.

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