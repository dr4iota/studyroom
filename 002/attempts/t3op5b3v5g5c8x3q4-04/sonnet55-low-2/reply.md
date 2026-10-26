All three asked values are constrained by the reads that returned 0.

**Q2 (B2).** Only A3 and B3 write to x. B3 writes whatever B2 returned. Suppose B2 returned a nonzero value. It could only have come from A3, which would have to take effect before B2. B3 would then write that same nonzero value. B4 comes after B3 and reads x, so it would see a nonzero value, but B4 is known to return 0. This is a contradiction, so B2 must return 0.

**Q1 (A4).** The writes to z are B1 (5), C2 (5) and C3 (1), with C2 before C3. The possible orders give z the value sequences 0,5,5,1 or 0,5,1,5. A4 can therefore read 0, 5 or 1.
- A3 writes A1's value to x. B4 and C4 both read 0, so A3 must write 0 or take effect after both reads.
- If A1 reads 0, A3 writes 0 and nothing is violated.
- A1 can read 0 in every case. A1 and A4 sit on either side of A2 and A3, so A4 can still read 0, 5 or 1.
- All three values are therefore possible for A4.

**Q3 (final y).** C1 writes 4 and A5 writes 3, and A5 comes after A4. Both orders are achievable, even when A4 reads 0 (A5 can fall before C2). The final value of y can be 3 or 4 for each A4 value.

With B2 fixed at 0, the combinations are A4 ∈ {0, 1, 5} crossed with y ∈ {3, 4}.

BEGIN
0 0 3
0 0 4
1 0 3
1 0 4
5 0 3
5 0 4
END