**Reasoning summary**

- **y-writes:** A1 and B3 both write 1. C1 reads 0, so C1 must take effect before A1. B3 comes after B2 ends, which is after Q, so B3 is late.
- **D3 (Q2):** It returns 0 if it takes effect before A1 (and B3), and 1 otherwise. D3 returns 0 only if D1 < D2 < D3 < A1 < A2, which means D2 has already written 1 to x before A2.
- **x-writes:** B1 writes 2, C2 writes 2, C3 writes 3, C4 writes 2 (with C2 < C3 < C4 < Q), and D1 writes 3, D2 writes 1, D4 writes 1 (with D1 < D2 < D4).
- **A2 (Q1):** It reads x after A1. Each value 0, 1, 2, 3 can be the latest x-write before A2. A2 = 0 requires every x-write to come after A2, so D3 comes after A1 and D3 = 1.
- **Final x (Q3):** C3 and D1 can never be last, because C4 and D2/D4 follow them in their threads. The final value is therefore 1 (D4 last) or 2 (B1 or C4 last).
- **Joint feasibility:** Every combination is achievable except A2 = 0 with D3 = 0, which is impossible for the reason above. That leaves 4 × 2 × 2 − 2 = 14 combinations.

BEGIN
0 1 1
0 1 2
1 0 1
1 0 2
1 1 1
1 1 2
2 0 1
2 0 2
2 1 1
2 1 2
3 0 1
3 0 2
3 1 1
3 1 2
END