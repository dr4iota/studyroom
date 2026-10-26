Each operation takes effect at a single instant, so every execution is a sequential interleaving of A1–A4 and B1–B4 that keeps each thread's own order. Let a be the value A1 reads. A4 writes a to x, and A1 can only see B's writes, so a ∈ {0, 1, 3}.

**Case a = 0** (A1 runs before B1). A3 comes before A4, and A3 can read 0 (before B1), 1 (between B1 and B2) or 3 (after B2). A4 writes 0 once, so B3 and B4 can be:
- (3,3), if A4 comes after B4 or before B2.
- (3,0), if A4 falls between B3 and B4.
- (0,0), if A4 falls between B2 and B3.

(0,3) is impossible because A4 writes only once. Each A3 value works with all three pairs, so this gives 9 combinations.

**Case a = 1** (A1 runs between B1 and B2). A3 reads 1 (before B2) or 3 (after B2), and A4 writes 1. B3 and B4 can be (3,3), (3,1) or (1,1). Both A3 values work with all three pairs, so this gives 6 combinations.

**Case a = 3** (A1 runs after B2). A3 reads 3, A4 writes 3, and B3 and B4 both read 3. This gives 1 combination, 3 3 3, which already appears in the a = 0 and a = 1 cases.

BEGIN
0 3 3
0 3 0
0 0 0
1 3 3
1 3 0
1 0 0
3 3 3
3 3 0
3 0 0
1 3 1
1 1 1
3 3 1
3 1 1
END