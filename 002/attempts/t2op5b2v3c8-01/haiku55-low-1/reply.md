Thread B's reads r1 and r2 both happen before B's first write (B3), so only A's writes to x (3, then 1) can affect them. The final y is whatever A3 reads, since A4 is the only writer of y. Enumerating every order-preserving interleaving of A's and B's operations gives these 12 distinct outcomes (Q1 = r1, Q2 = r2, Q3 = final y):

BEGIN
0 0 0
0 0 1
0 3 0
0 3 1
0 3 3
3 3 1
3 3 3
0 1 0
0 1 1
3 1 1
3 1 3
1 1 1
END