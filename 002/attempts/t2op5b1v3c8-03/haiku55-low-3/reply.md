Without sync points, the only constraints are program order within each thread and that each operation takes effect at one instant. So every interleaving of the two 5-operation sequences is possible.

Let k be the number of A operations that have taken effect before a given point. The last write visible at that point is:

| k | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| value | 0 | 2 | 3 | 1 | 3 | 3 |

- **B3** is read at some k₃ (0 to 5), so it can be 0, 1, 2, or 3. B2 is read earlier at k₂ ≤ k₃, so B2's value is lastwrite(k₂).
- **B4 and B5** write B2's value. For A5 to return something other than 3, a B write must fall between A4 and A5, which forces B4/B5 to occur at k = 4 and B3 to occur at k₃ ≤ 4.
- **A5** returns 3 if no B write lands between A4 and A5. Otherwise it returns B2's value.

Checking which pairs (A5, B3) are jointly achievable:

- A5 = 3 (no B write before A5): B3 can be any of 0, 1, 2, 3, with k₂ = k₃.
- A5 = 0 (k₂ = 0): B3 ∈ {0, 1, 2, 3}.
- A5 = 2 (k₂ = 1, so k₃ ≥ 1): B3 ∈ {1, 2, 3}.
- A5 = 1 (k₂ = 3, so k₃ ∈ {3, 4}): B3 ∈ {1, 3}.

The pair (1, 0) and the pair (2, 0) are impossible, since B3 = 0 requires k₃ = 0 and that forces A5 = 3.

BEGIN
0 0
0 1
0 2
0 3
1 1
1 3
2 1
2 2
2 3
3 0
3 1
3 2
3 3
END