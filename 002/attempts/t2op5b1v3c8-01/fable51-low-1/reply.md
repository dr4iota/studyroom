**Analysis:** A's writes make x monotone (1,1,2,3). B2's value v is written back by B3 and B5. So B1 ≤ v ≤ B4, and the final value is either 3 (if B5 precedes A4) or v (if B5 is last). If B4 returned 3, A4 already happened, so the final value must be v (which then equals 3 only if v = 3).

BEGIN
0 0 0
0 1 0
0 2 0
0 3 0
0 1 1
0 2 1
0 3 1
1 1 1
1 2 1
1 3 1
0 2 2
0 3 2
1 2 2
1 3 2
2 2 2
2 3 2
0 0 3
0 1 3
0 2 3
0 3 3
1 1 3
1 2 3
1 3 3
2 2 3
2 3 3
3 3 3
END