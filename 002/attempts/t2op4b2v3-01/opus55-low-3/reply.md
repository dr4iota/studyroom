Thread B writes x in a fixed order, so x takes the values **0 → 3 → 2 → 1**, in that order.

Thread A's reads happen one after another. So each read sees the same value as the previous read, or a later one in that sequence. Value positions: 0 is position 0, 3 is position 1, 2 is position 2, 1 is position 3.

1. A1's position ≤ A2's position ≤ A3's position ≤ A4's position.
2. A3 can always take a value between A2 and A4, so it adds no further restriction.
3. Any choice of positions i ≤ j ≤ k for A1, A2 and A4 can happen. Thread A just interleaves its reads between B's writes as needed.

This gives C(6,3) = 20 combinations.

BEGIN
0 0 0
0 0 3
0 0 2
0 0 1
0 3 3
0 3 2
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 2
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END