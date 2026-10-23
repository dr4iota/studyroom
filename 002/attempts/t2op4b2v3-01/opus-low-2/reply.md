Thread B's writes take effect in program order, so x holds 0, then 3, then 2, then 1 over time. Thread A's reads also take effect in order, so each read sees a value at the same stage or a later stage than the read before it.

Number the stages 0, 1, 2, 3, holding values 0, 3, 2, 1. A1, A2 and A4 return values at stages i ≤ j ≤ k. A3 is not asked, and it can always fit between A2 and A4. That gives every non-decreasing triple over 4 stages, which is C(6,3) = 20 combinations.

BEGIN
0 0 0
0 0 3
0 0 2
0 0 1
0 3 3
0 3 2
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 2
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END