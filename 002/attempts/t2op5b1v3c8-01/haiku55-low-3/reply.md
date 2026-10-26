Let k be the number of A-writes that have taken effect at a given instant (values 1, 1, 2, 3 for k = 1..4). Reads return val(k), where val(0)=0, val(1)=1, val(2)=1, val(3)=2, val(4)=3. Let k1 ≤ k2 ≤ k3 ≤ k4 ≤ k5 be the A-counts at B1, B2, B3, B4, and B5. Then:

- Q1 = val(k1).
- v2 = val(k2) is the value B3 and B5 write.
- Q2 = v2 if B3 is the last write before B4 (k4 = k3), otherwise val(k4).
- Q3 = v2 if all A-writes precede B5 (k5 = 4), otherwise 3, since a4 is then the last write.

Enumerating by k2 gives 26 distinct outcomes:

- Q1=0: (0,0,0), (0,0,3), (0,1,0), (0,1,1), (0,1,3), (0,2,0), (0,2,1), (0,2,2), (0,2,3), (0,3,0), (0,3,1), (0,3,2), (0,3,3)
- Q1=1: (1,1,1), (1,1,3), (1,2,1), (1,2,2), (1,2,3), (1,3,1), (1,3,2), (1,3,3)
- Q1=2: (2,2,2), (2,2,3), (2,3,2), (2,3,3)
- Q1=3: (3,3,3)

BEGIN
0 0 0
0 0 3
0 1 0
0 1 1
0 1 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 2
0 3 3
1 1 1
1 1 3
1 2 1
1 2 2
1 2 3
1 3 1
1 3 2
1 3 3
2 2 2
2 2 3
2 3 2
2 3 3
3 3 3
END