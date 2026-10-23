All operations are unconstrained by sync points, so the threads interleave freely. A1 can see 0 (before B1), 3 (after B1, before B3), or 2 (after B3). A5 sees 0 or 4 depending on B5's order; B4 sees 0 or 1 depending on A4's order. Each pair of (A5, B4) outcomes is realizable (e.g., A4<B4<B5<A5 gives 4/1; B4<A4<A5<B5 gives 0/0; all of B before A4 gives 4/0; A4<B4 with A5<B5 gives 0/1), and in each case A1 can be placed relative to B1/B3 to get any of its three values.

BEGIN
0 0 0
0 0 1
0 4 0
0 4 1
3 0 0
3 0 1
3 4 0
3 4 1
2 0 0
2 0 1
2 4 0
2 4 1
END