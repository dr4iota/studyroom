All interleavings of A's sequence (W1, R, R) and B's sequence (R, W3, W2) are allowed.

- B1 returns 0 (if it takes effect before A1) or 1 (if after A1).
- A2 and A3 both happen after A1, and the writes that can land after A1 are B2 (3) then B3 (2), in that order. So the reads see values advancing along 1 → 3 → 2, giving (A2, A3) ∈ {(1,1), (1,3), (1,2), (3,3), (3,2), (2,2)}.
- Each of these pairs is compatible with B1 = 0 (B1 before A1) and with B1 = 1 (B1 after A1), since B2/B3 can still be placed anywhere relative to A2/A3 in both cases.

BEGIN
1 1 0
1 3 0
1 2 0
3 3 0
3 2 0
2 2 0
1 1 1
1 3 1
1 2 1
3 3 1
3 2 1
2 2 1
END