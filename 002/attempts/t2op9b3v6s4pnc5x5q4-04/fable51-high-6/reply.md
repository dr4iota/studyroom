**Analysis**

- **z / A4:** A4 reads z after both B1 (=1, before P) and A1 (=6, program order). A1 and B1 are unordered, so A4 ∈ {1, 6}. A6/A7/A8/A9 all propagate A4's value, so final **y = A4** (A8 is the only write to y).
- **Final z and B9:** B8 (after R) is the last write to z and writes B2's value; B9 reads it. B2 reads y, which is 0 unless A8 already happened. A8 can be before B2 (A8 < B2 < Q < A9 is allowed), so B2 ∈ {0, A4}. Hence **B9 = final z = B2**.
- **Final x:** Last write to x is B7 (=4) unless A2 (=1) lands after B7, which is allowed (A2 is only bound by program order). But if B2 = A4 (i.e., A8 < B2 < B5 < B7), then A2 < A8 < B7, so x must be 4. If B2 = 0, x ∈ {1, 4}.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END