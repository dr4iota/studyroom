Each thread's operations are sequential, and with no sync points the two threads can interleave arbitrarily. So the outcomes depend only on how many of A's operations have completed before each of B's reads and writes.

Let p1 ≤ p2 ≤ p3 ≤ p4 ≤ p5 (each in 0..5) be the number of A operations completed before B1, B2, B3, B4, B5. Every such sequence is a valid interleaving.

- **B1 reads y:** y is 0 if p1=0, 2 if p1=1, and 1 if p1≥2. Call this value f(p1).
- **x writes:** A4 writes 3 and B2 writes f(p1). Then B3 reads 3 exactly when A4 falls between B2 and B3 (p2<4≤p3). Otherwise B3 reads f(p1). B5 reads 3 exactly when p2<4≤p5, and f(p1) otherwise.
- **Final y:** A5 writes 1 last among A's y-writes. B4 overwrites y with B3's value only if it runs after A5 (p4=5). Otherwise the final y is 1.

Enumerating the cases:

- **p2 ≥ 4:** Q1 = Q2 = f(p1) ∈ {0, 2, 1}. Final y is f(p1) if p4=5, else 1. This gives (0,0,0), (0,0,1), (2,2,2), (2,2,1), (1,1,1).
- **p2 < 4 ≤ p3:** Q1 = Q2 = 3. Final y is 3 if p4=5, else 1. This gives (3,3,3), (3,3,1).
- **p2 < 4 and p3 < 4, p5 ≥ 4:** Q1 = f(p1), Q2 = 3. Final y is f(p1) if p4=5, else 1. This gives (0,3,0), (0,3,1), (2,3,2), (2,3,1), (1,3,1).
- **p2 < 4 and p5 < 4:** Q1 = Q2 = f(p1), final y = 1. This gives (0,0,1), (2,2,1), (1,1,1), all already listed.

That gives 12 distinct combinations.

BEGIN
0 0 0
0 0 1
2 2 2
2 2 1
1 1 1
3 3 3
3 3 1
0 3 0
0 3 1
2 3 2
2 3 1
1 3 1
END