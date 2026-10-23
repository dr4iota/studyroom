With no sync points, the only constraints are program order within each thread. Operations of different threads can overlap arbitrarily, so any interleaving of the effect instants that respects program order is possible. Two facts simplify the analysis:

- **A2 and B2 don't affect the asked values**, so only A1, B1, B3, B4, B5, A3, and A4 matter.
- **A1** returns 1 if B1 takes effect before it, and 0 otherwise. No other write can precede A1, since A3 and A4 come after it.
- **B3** returns 1, 2, or 3 depending on the latest of A3 and A4 that takes effect before it (B1 always precedes B3).
- **B5** returns the latest of B4 (value 1), A3 (value 2), and A4 (value 3) that takes effect before it.

Enumerating the orderings gives these combinations for (A1, B3, B5). Each is realized by an explicit interleaving, and the combinations B3=2 with B5=2 and B3=3 with B5=2 are impossible because A3 and A4 would then have to fall after B4, which contradicts B3's value.

BEGIN
0 1 1
0 1 2
0 1 3
0 2 1
0 2 3
0 3 1
1 1 1
1 1 2
1 1 3
1 2 1
1 2 3
1 3 1
END