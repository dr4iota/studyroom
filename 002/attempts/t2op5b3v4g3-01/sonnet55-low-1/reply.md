Each thread runs in order, so A1<A2<A3<A4<A5 and B1<B2<B3<B4<B5.

**A1.** A3 returns 4, and only B1 writes 4 to y. So B1 takes effect before A3. A1 comes before A3, so it can fall on either side of B1. It returns 0 if it is before B1, or 4 if it is after B1. Both are possible.

**B2 and B3.** Both reads come before B5, so B5 never affects them. The only writes to z that matter are A2 (3) and then A4 (4), in that order. The value of z over time is 0, then 3, then 4. B2 comes before B3, so the pair (B2, B3) follows this timeline without going backward. The possible pairs are (0,0), (0,3), (0,4), (3,3), (3,4) and (4,4).

**Combining.** The two choices are independent, so every combination is feasible.
- For A1=4, we need B1<A1<A2, which is compatible with B2 and B3 reading anywhere on the z timeline.
- For A1=0, we need A1<B1<A3. B2 and B3 can still be placed before A2, between A2 and A4, or after A4. For (4,4), B1<A3<A4<B2 works.

That gives 2 × 6 = 12 combinations.

BEGIN
0 0 0
0 0 3
0 0 4
0 3 3
0 3 4
0 4 4
4 0 0
4 0 3
4 0 4
4 3 3
4 3 4
4 4 4
END