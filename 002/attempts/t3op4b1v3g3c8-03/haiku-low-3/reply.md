The possible outcomes are the 29 combinations below, in the order Q1 (B2's value), Q2 (C1's value), Q3 (final x).

Each operation takes effect at an instant, and each thread's operations take effect in listed order, so any outcome corresponds to a total order of the operations that respects the thread orders. B1 returning 1 constrains where B1 can fall. I then grouped the cases by C1's value (0, 1, 2, or 3) and checked which B2 and final values can follow in each case. I checked each listed triple against a concrete ordering, but the case analysis was done by hand and not mechanically verified.

BEGIN
0 0 0
0 0 2
1 0 0
1 0 1
1 0 2
1 1 1
1 1 2
1 2 1
1 2 2
1 3 1
1 3 2
1 3 3
2 0 0
2 0 2
2 1 1
2 1 2
2 2 2
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 1 1
3 1 2
3 1 3
3 2 2
3 2 3
3 3 2
3 3 3
END