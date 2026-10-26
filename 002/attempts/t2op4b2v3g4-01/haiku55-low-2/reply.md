Thread A has A1 (reads y, always 0), then A2 and A3 (reads of x), then A4 (write 2 to x). Thread B has B1 (read x, known to return 0), then B2 (write 3), B3 (write 2), and B4 (write 1).

Since B1 returned 0 and comes before every write in B, A4 must take effect after B1. A2 and A3 must both take effect before A4.

**Reads of x.** Let k be the number of B writes that have taken effect before a given read. The read then returns the value of the k-th write in B's sequence: k=0 gives 0, k=1 gives 3, k=2 gives 2, k=3 gives 1. Since A2 is before A3, k2 ≤ k3.

**Final value.** Let m be the number of B writes before A4, with k3 ≤ m. If m=3, A4 is last, so the final value is 2. If m<3, B4 comes after A4, so the final value is 1.

**Enumeration.**
- m=3 (final 2): all pairs with k2 ≤ k3 ≤ 3 are possible, giving 10 outcomes.
- m=0, 1, 2 (final 1): the pairs with k3 ≤ m are possible. Their union gives 6 distinct outcomes: (0,0), (0,3), (3,3), (0,2), (3,2), (2,2) for (A2, A3).

That gives 16 combinations in total.

BEGIN
0 0 2
0 3 2
0 2 2
0 1 2
3 3 2
3 2 2
3 1 2
2 2 2
2 1 2
1 1 2
0 0 1
0 3 1
3 3 1
0 2 1
3 2 1
2 2 1
END