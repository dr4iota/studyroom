Constraints on x:
- A1 reads 0, so A1 takes effect before B1. B1 is the first write to x, and A5 comes after A1 in program order.
- B2 reads 2, so no write of 4 (A5) can take effect between B1 and B2. A5 either takes effect before B1 or after B2.

Case 1: A5 takes effect before B1.
- A3 and A4 come before A5, which comes before B1, and B3 and B4 come after B1, so both reads return 0.
- B5 is the last write to x, so the final x is 2.

Case 2: A5 takes effect after B2.
- A3 and A4 come before A5, so they can interleave freely with B3 (writes 1) and B4 (writes 3).
- Since A3 takes effect before A4, the y values are non-decreasing in the order 0, 1, 3. The possible pairs are (0,0), (0,1), (0,3), (1,1), (1,3), (3,3).
- A5 can take effect after B4 but before B5, giving a final x of 2. It can also take effect after B5, giving a final x of 4.
- Both final values are possible with every pair.

Combining the cases gives every pair with final x = 2 or 4.

BEGIN
0 0 2
0 0 4
0 1 2
0 1 4
0 3 2
0 3 4
1 1 2
1 1 4
1 3 2
1 3 4
3 3 2
3 3 4
END