All 27 combinations are reachable, since there are no sync points and each requested value can be arranged independently (e.g. final y = 0 via A1 reading 0 and A2/A4 overwriting B1's 1 before B2 reads; final y = 3 via B2 reading after D1 with B3 last; final y = 1 via D2 last).

BEGIN
0 0 0
0 0 1
0 0 3
0 1 0
0 1 1
0 1 3
0 3 0
0 3 1
0 3 3
1 0 0
1 0 1
1 0 3
1 1 0
1 1 1
1 1 3
1 3 0
1 3 1
1 3 3
3 0 0
3 0 1
3 0 3
3 1 0
3 1 1
3 1 3
3 3 0
3 3 1
3 3 3
END