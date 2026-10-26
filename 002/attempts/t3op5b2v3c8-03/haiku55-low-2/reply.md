This is an enumeration over interleavings of the 14 operations, respecting each thread's order. I worked it out by reasoning about the constraints rather than brute-forcing all 252,252 interleavings.

**Key facts:**
- **B2 always sees 1 or 2.** B1 precedes B2 in program order, so the last y-write before B2 is B1 (value 2), unless C4 (value 1) lands between B1 and B2.
- **A3 can see 0, 1, or 2**, and every (A3, final y) pairing is achievable.
- **Final y is 1 or 2.** It is 1 if C4 is the last y-write, otherwise it equals B2's value (B3 writes it).
- **Final x** is the last write of A5 (3), B5 (B2's value), or C2 (C1's value). C2 is the only way to get 0.
- **If C2 is the last x-write**, C4 must come after C2, which forces A3 < C4 and B3 < C4. Then final y = 1, B2 reads 2, and A3 reads 0 or 2 (never 1).

**Combinations by case:**
- **Final x = 3 (A5 last):** all six (A3, final y) pairs are achievable, with A5 placed at the end.
- **Final x = B2's value (B5 last):** final x = 1 requires final y = 1 and A3 can be 0, 1, or 2; final x = 2 allows final y of 1 or 2 with A3 of 0, 1, or 2.
- **Final x = C1's value (C2 last):** only final x ∈ {0, 1, 2, 3} with A3 ∈ {0, 2} and final y = 1 are achievable; each of these four values is reachable.

Combining these gives 17 distinct outcomes.

BEGIN
0 0 1
0 1 1
0 2 1
0 2 2
0 3 1
0 3 2
1 1 1
1 2 1
1 2 2
1 3 1
1 3 2
2 0 1
2 1 1
2 2 1
2 2 2
2 3 1
2 3 2
END