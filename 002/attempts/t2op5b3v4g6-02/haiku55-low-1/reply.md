The possible outcomes are the 6 feasible (A3, A4) pairs crossed with the 2 possible final values of x, giving 12 combinations.

**Constraints on x:**
- A1 reads 0, so A1 takes effect before B1 (the first write of 2 to x).
- B2 reads 2, so B1 < B2 and A5 (which writes 4) cannot take effect between B1 and B2.
- The final x is whichever of B5 (2) and A5 (4) takes effect last. Final x can be 4 (A5 after B5) or 2 (A5 before B5, either before B1 or between B2 and B5).

**Values of y:** y starts at 0, is written 1 by B3 and then 3 by B4. A3 and A4 read in order, so their values are non-decreasing through the sequence 0, 1, 3. The allowed pairs are (0,0), (0,1), (0,3), (1,1), (1,3), (3,3).

**Feasibility:** Each y-pair can be realized with final x = 4 (A3 and A4 happen before A5, which happens after B5) and with final x = 2 (A5 placed between B2 and B5, with A3 and A4 before it). The x-constraints do not restrict the y-reads, so all 6 × 2 = 12 combinations are possible.

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