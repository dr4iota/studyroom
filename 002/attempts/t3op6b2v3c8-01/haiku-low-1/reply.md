Q1 is the value returned by A4, Q2 is the value returned by B5, and Q3 is the final value of x. There are no sync points, so any interleaving of the 15 operations that respects each thread's order is allowed.

Key facts:
- Only 0 and 2 ever appear in x, since every write to x is 2 or a value read from x. So Q1 and Q3 are in {0, 2}.
- B5 reads y. Its value is B2's value (the B3 write) unless C2's write of 1 falls between B3 and B5, in which case it is 1. So Q2 is in {0, 1, 2}.

I checked each of the 12 combinations by constructing an explicit interleaving:
- **B2 reads 0** (needs A3 and A4 before B1, A5 between B1 and B2): gives Q2 in {0, 1} with Q1 in {0, 2} and Q3 in {0, 2}, all 8 combinations.
- **B2 reads 2**: gives Q2 in {1, 2}, with Q1 in {0, 2} and Q3 in {0, 2}, all 8 combinations.

Together these cover all 2 × 3 × 2 = 12 combinations of Q1, Q2 and Q3 with each Q in its possible range.

BEGIN
0 0 0
0 0 2
0 1 0
0 1 2
0 2 0
0 2 2
2 0 0
2 0 2
2 1 0
2 1 2
2 2 0
2 2 2
END