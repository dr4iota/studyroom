Every combination of Q1 (the value A3 returns), Q2 (final x), and Q3 (final y) is possible, giving 24 outcomes. The problem gives no known read results, so every interleaving that respects each thread's order is allowed.

**Key facts**
- B2 always runs after B1, so B2 reads 1 or 2 (1 only if C4 lands between B1 and B2). Final y is therefore 1 or 2, and B3 writes the value B2 read.
- A3 can read 0, 1, or 2, depending on whether its last y-write before it is none, C4, B1, or B3.
- A4 always precedes A5 and A5 writes 3, so A4's value never survives. Final x is the last of A5, B5, or C2, which gives 3, v2, or v1. The value v1 read by C1 can be 0, 1, 2, or 3, so final x is in {0, 1, 2, 3}.

**Feasibility**
Final x is determined by where A5, B5, and C2 sit, while A3's value and final y depend on where B1, B2, B3, C4, and A3 sit. Both can be set independently by placing the x-writers at the start or end of the schedule. For each final x value (0 via C2 last with C1 first, 1 via C2 last after C1 reads A1's 1, 2 via B5 last with v2 = 2, and 3 via A5 last), all six combinations of A3's value and final y can be realized. Hence all 3 × 4 × 2 = 24 triples occur.

BEGIN
0 0 1
0 0 2
0 1 1
0 1 2
0 2 1
0 2 2
0 3 1
0 3 2
1 0 1
1 0 2
1 1 1
1 1 2
1 2 1
1 2 2
1 3 1
1 3 2
2 0 1
2 0 2
2 1 1
2 1 2
2 2 1
2 2 2
2 3 1
2 3 2
END