The possible outcomes are the 12 combinations below, listed as (Q1, Q2, Q3) = (value of A1, value of A4, final y).

Key facts used:
- A1 can only read 0, 1, or 3, since A2 (which writes 2) comes after A1 in program order.
- B5 always follows B4, so B4 can only read A3's value or 0. This makes B6's value either A3's value or 0.
- The final y is either A3's value or B6's value, never 2.
- B3 reading 3 requires the last x-write before B3 to be B2 or A5.

BEGIN
0 0 0
0 2 0
1 0 0
1 1 0
1 1 1
1 2 0
1 2 1
3 0 0
3 2 0
3 2 3
3 3 0
3 3 3
END