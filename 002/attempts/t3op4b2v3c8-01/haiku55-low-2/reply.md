I modeled each execution as a total order of the 10 operations that respects each thread's order, then computed the values each read returns and checked the consistency of the written values. This gives 15 achievable (Q1, Q2, Q3) combinations.

Q3 (C1) can only be 0 or 2, since C4 comes after C1 and only B2 can have written y before it. Q2 (B3) is 2 unless C4 lands between B2 and B3, in which case it is C3's value. Q1 (A1) can be 0, 2, or C3's value, and C3's value can be 0, 2, or 3.

Each combination below has a witnessing ordering. For example, `3 3 0` comes from B1, C1, C2, C3 (reads x=3), B2, C4 (writes 3 to y), A1 (reads 3), B3 (reads 3).

BEGIN
0 0 0
2 0 0
0 2 0
0 3 0
2 2 0
2 3 0
3 2 0
3 3 0
0 2 2
2 2 2
3 2 2
0 3 2
2 3 2
3 3 2
0 0 2
END