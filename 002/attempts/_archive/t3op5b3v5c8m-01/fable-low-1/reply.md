**Analysis:** Only x matters. Writes to x: A4 (5), B1 (4), C4 (1); A5 follows A4, C5 follows C4; no sync constraints. Enumerating all interleavings:

- A4 last (final 5): A5=5; C5 ∈ {1,4,5}
- C4 last (final 1): C5=1; A5 ∈ {5,4,1}
- B1 last (final 4): A5=5 → C5 ∈ {1,4,5}; A5=1 → C5 ∈ {1,4}; A5=4 → C5 ∈ {1,4,5}

BEGIN
5 1 5
5 4 5
5 5 5
5 1 1
4 1 1
1 1 1
5 1 4
5 4 4
5 5 4
1 1 4
1 4 4
4 1 4
4 4 4
4 5 4
END