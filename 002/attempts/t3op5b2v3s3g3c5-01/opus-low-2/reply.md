Every pair with Q1 ≤ Q2 is possible, combined with either value of Q3. That gives 12 combinations.

**1. Only C writes before B1.** B1 reads y = 0, so B1 takes effect before C1. The writes to y are C1 (1), C2 (2) and B3 (2). Thread C finishes before P, and B3 comes after B1. So y goes 0 → 1 (at C1) → 2 (at C2), and every later write keeps it at 2.

**2. y never decreases.** Because y only moves 0 → 1 → 2, any later read of y returns a value at least as large as an earlier read.

**3. A1 and A2 (Q1, Q2).** Each can read 0, 1 or 2, with the condition A1 ≤ A2. Thread A only has to finish A1–A4 before Q, so A1 and A2 can sit before C1, between C1 and C2, or after C2. A2 must end after R, and R comes after B1. That still lets A2 read 0 by taking effect before C1. A3 = 2 and B4 = 2 are always satisfiable later. This gives 6 pairs: (0,0), (0,1), (0,2), (1,1), (1,2), (2,2).

**4. B2 (Q3).** B2 comes after B1 and before B3. It reads 0 if it takes effect before C3 (C's write of 1 to x), and 1 if after. A5's write of 1 to x is not needed for the 1 case, but it does not change the result either.

**5. Independence.** Thread A's reads are placed relative to C1 and C2. B2 is placed relative to C3. Nothing ties these placements together, so each of the 6 pairs combines with either value of B2.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 1 0
1 1 1
1 2 0
1 2 1
2 2 0
2 2 1
END