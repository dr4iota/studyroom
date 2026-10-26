The possible outcomes come from the write orders on y and the timing of z.

- **z:** Only B4 writes z (to 1), and B5 reads 1, so B4 happens before B5. A1 and A5 each read 0 if they happen before B4 and 1 if after. A5 can take either value, since A5 can be placed before or after B4 without conflicting with anything else.
- **y writes:** A2 (1) comes before A3 (3) in thread A. B3 (1) can go anywhere. The three possible orders are:
  - A2, A3, B3: y is 0, 1, 3 before B3.
  - A2, B3, A3: y is 0, 1 before B3, then 3.
  - B3, A2, A3: y is 0 before A2.
- **B1, B2:** Both happen before B3 and in time order. Their possible pairs of values, respecting that y only moves through the states above in order, are (0,0), (0,1), (0,3), (1,1), (1,3), (3,3). Each is realizable: for example, (3,3) uses A2, A3, B1, B2, B3, and (0,3) puts B1 before A2 and B2 after A3.

Q1 is independent of the B1/B2 pairs, so every pair appears with both values of Q1. That gives 2 × 6 = 12 combinations.

BEGIN
0 0 0
0 0 1
0 0 3
0 1 1
0 1 3
0 3 3
1 0 0
1 0 1
1 0 3
1 1 1
1 1 3
1 3 3
END