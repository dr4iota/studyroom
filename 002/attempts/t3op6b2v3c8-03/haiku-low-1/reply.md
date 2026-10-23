The possible outcomes are the 16 triples below, in the order (Q1, Q2, Q3) = (A2, B1, C4). Each thread's operations take effect in program order, and the three threads interleave freely.

**Key facts:**
- Every value is 0, 2, or 3.
- The value 2 can reach x only through B4, which writes B2's read of y. So 2 appears in x only if B2 reads 2, which requires A1 or A3 to run before B2 and A6 to run after it.
- Once x has been written with a nonzero value, 0 can reappear only through B4 writing 0. That requires B2 to read 0, meaning B2 runs before A1 (or A6 has copied a 0 into y).
- c (B1) is 0 if B1 precedes C1 and 3 otherwise.

**Two regimes:**
- **B2 reads 2:** a can be 0, 2, or 3 (A2 can be placed wherever x has that value), and c and g are each 0 or 3 for c, and 2 or 3 for g. This gives 12 triples.
- **B2 reads 0 or a:** x only ever holds 0 or 3, so a, c, g ∈ {0, 3}. Of these eight triples, four have g = 3 and are already counted above. The other four are (0,0,0), (0,3,0), (3,0,0), and (3,3,0), each shown feasible by an explicit schedule.

BEGIN
0 0 0
0 0 2
0 0 3
0 3 0
0 3 2
0 3 3
2 0 2
2 0 3
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 3 0
3 3 2
3 3 3
END