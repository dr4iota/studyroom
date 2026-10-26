**Known results:** A1 = 0, A2 = 0 (z is never written), B2 = 2.

**Constraints on x:**
- A1 reads 0, so A1 takes effect before B1 (and before A5, by program order).
- B2 reads 2, and B1 precedes B2 in program order. So A5 must not take effect between B1 and B2. Either A5 < B1, or A5 > B2.
- The final x is the value of the latest of the writes B1 (2), A5 (4), and B5 (2). B5 always comes after B2.
  - If A5 < B1: B5 is last, so final x = 2.
  - If A5 > B2 and A5 < B5: final x = 2.
  - If A5 > B5: final x = 4.

**Constraints on y:** B3 (writes 1) takes effect before B4 (writes 3). Over time, y reads 0, then 1, then 3. Since A3 precedes A4, the pair (A3, A4) must be non-decreasing in that order. That gives six candidates: (0,0), (0,1), (0,3), (1,1), (1,3), (3,3).

**Feasibility:**
- If A5 < B1, both A3 and A4 must come before B3, so they read 0. This yields (0,0) with final x = 2.
- If A5 > B2, A5 can be placed after B4 and B5 or anywhere in between. A3 and A4 can be placed freely before A5, so every y pattern is achievable. Both final values 2 and 4 are achievable too.

So every pair of y-reads combines with both final x values, giving 6 × 2 = 12 outcomes.

Values are in the order Q1 Q2 Q3 (A3, A4, final x):

BEGIN
0 0 2
0 0 4
0 1 2
0 1 4
0 3 2
0 3 4
1 1 2
1 1 4
1 3 2
1 3 4
3 3 2
3 3 4
END