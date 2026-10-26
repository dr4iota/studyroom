The execution space is every interleaving of A1–A5 with B1–B4 that respects each thread's order, since the problem gives no sync points. A quick enumeration gives 26 distinct outcomes.

Let g_i be the number of A operations that finish before B_i. The value of x after k A operations (with no B4 yet) is V(k) = [0, 3, 1, 1, 1, 2] for k = 0..5. B1, B2, and B3 all read before B4, so each equals V of its gap. B4 writes B2's value, and A5 always overwrites x with 2 unless B4 comes after A5, so the final value is 2 when g4 ≤ 4 and V(g2) when g4 = 5. The value A3 reads only feeds A4's write, which A5 always overwrites, so it doesn't affect the asked values.

Enumerating the gap orderings g1 ≤ g2 ≤ g3 ≤ g4 gives these (Q1, Q2, Q3) outcomes:

BEGIN
0 0 0
0 0 2
0 1 0
0 1 1
0 1 2
0 1 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 2
0 3 3
1 1 1
1 1 2
1 2 1
1 2 2
2 2 2
3 1 1
3 1 2
3 1 3
3 2 1
3 2 2
3 2 3
3 3 2
3 3 3
END