I modeled each execution as an interleaving of A1–A5 and B1–B5 that preserves each thread's order. That gives 252 interleavings, and I grouped them by where the B operations fall among the A operations.

Key facts:
- B1 reads y: 0 if no A op has run, 2 if only A1 has run, 1 once A2 has run.
- B3 returns 3 only if A4 falls between B2 and B3. Otherwise it returns the value B2 wrote.
- B5 returns 3 only if A4 falls between B2 and B5. Otherwise it returns the value B2 wrote.
- Final y is r3 if B4 runs after A5, and 1 otherwise, since A5 is the last write to y from A.

Enumerating the cases gives these (Q1, Q2, Q3) outcomes:

BEGIN
0 0 0
0 0 1
0 3 0
0 3 1
1 1 1
1 3 1
2 2 1
2 2 2
2 3 1
2 3 2
3 3 1
3 3 3
END