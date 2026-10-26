The writes in B are ordered, so x passes through the sequence 0, 3, 2, 1. A's reads are ordered too, so each read returns a value at or after the position of the previous read in that sequence. Reads are monotone non-decreasing in position.

A1, A2, A3, A4 take effect in order, and each sees the state at its own instant. The positions are 0 (value 0), 1 (value 3), 2 (value 2) and 3 (value 1). Any non-decreasing position sequence p1 ≤ p2 ≤ p3 ≤ p4 is achievable, because B's writes can be interleaved anywhere between the reads.

The asked values are (p1, p2, p4), with p3 free. For each non-decreasing triple p1 ≤ p2 ≤ p4, we can pick p3 between p2 and p4, so every such triple is possible.

Mapping positions to values (0→0, 1→3, 2→2, 3→1), I list the triples with p1 ≤ p2 ≤ p4 over positions 0..3:

- p1=0:
  - p2=0: p4=0,1,2,3 → 0 0 0, 0 0 3, 0 0 2, 0 0 1
  - p2=1: p4=1,2,3 → 0 3 3, 0 3 2, 0 3 1
  - p2=2: p4=2,3 → 0 2 2, 0 2 1
  - p2=3: p4=3 → 0 1 1
- p1=1 (value 3):
  - p2=1: p4=1,2,3 → 3 3 3, 3 3 2, 3 3 1
  - p2=2: p4=2,3 → 3 2 2, 3 2 1
  - p2=3: 3 1 1
- p1=2 (value 2):
  - p2=2: p4=2,3 → 2 2 2, 2 2 1
  - p2=3: 2 1 1
- p1=3 (value 1):
  - 1 1 1

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