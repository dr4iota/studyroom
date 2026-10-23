Neither thread has a sync point, so any interleaving that keeps each thread's own order is allowed.

B2 and B3 are the only writes to x, and both write v, the value B1 read. So x only ever holds 0 or v, and the final value of x is v. Q3 is therefore v.

**B1's possible values**
- v = 0: B1 reads y before any write to y.
- v = 2: C2 wrote 2 before B1, and C5 had not yet written.
- v = 1: C5 wrote 1 before B1.

**Constraint from A3**
A3 returned 0. If v ≠ 0, A3 must happen before B2.

**Case v = 0**
- x is always 0, so C3 = 0.
- A4 can be 0 (before any y write), 2 (after C2 or B4), or 1 (after C5, when no later 2 has been written).
- Results (Q1, Q2, Q3): (0,0,0), (1,0,0), (2,0,0).

**Case v = 2**
- C3 can be 0 (before B2) or 2 (after B2). C3 = 2 is still before C5, which is the last op in C.
- A4 can be 0 (A3 and A4 both before C2), 1 (after C5), or 2.
- All six pairs of A4 and C3 can be realized.
- Results: (0,0,2), (0,2,2), (1,0,2), (1,2,2), (2,0,2), (2,2,2).

**Case v = 1**
- C5 happened before B1, so C2 and C3 happened before B1 and hence before B2. Therefore C3 = 0.
- A4 can be 0, 1, or 2.
- Results: (0,0,1), (1,0,1), (2,0,1).

BEGIN
0 0 0
1 0 0
2 0 0
0 0 2
0 2 2
1 0 2
1 2 2
2 0 2
2 2 2
0 0 1
1 0 1
2 0 1
END