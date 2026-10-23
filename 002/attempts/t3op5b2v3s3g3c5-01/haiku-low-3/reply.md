**Key constraints**

- **B1** reads 0, so no write to y happens before B1. Since B2 and B3 come after B1, the writes C1, C2, and B3 all come after B1.
- **A3** starts after A2 ends, and A2 ends after R, so A3 (and A4, A5) occur after R. The write by A5 to x therefore always comes after B2, which is before R. So B2 depends only on C3.
- **C4** reads 2, and C1 < C2 < C3 < C4 in thread C. The y-writes are C1 (1), C2 (2), and B3 (2), with B2 < B3 in thread B.

**Possible orders of the y-writes**

- (a) C1, C2, B3: y history 0→1→2→2
- (b) C1, B3, C2: y history 0→1→2→2
- (c) B3, C1, C2: y history 0→2→1→2

In (c), B3 precedes C1, C2, and C3, all of which come after B2. So B2 reads 0 in case (c). The same holds in case (b), since C3 follows C2, which follows B3. Only case (a) allows C3 to precede B2 (and B2 to precede B3), so B2 = 1 requires case (a).

**Values of A1 and A2**

A1 happens before A2's effect, and A2's effect can be placed at any time after A1 (A2's end can be pushed past R and before A3). So (Q1, Q2) = (value at t1, value at t2) with t1 < t2 along the y-history.

- History (a)/(b) (0→1→2): pairs (0,0), (0,1), (0,2), (1,1), (1,2), (2,2).
- History (c) (0→2→1→2): adds (2,1); all pairs from it are (0,0), (0,1), (0,2), (1,1), (1,2), (2,1), (2,2).

Pairs (1,0) and (2,0) are impossible because t1 < t2 would require a value to go back to 0.

**Combining with B2**

- B2 = 0 is possible with all seven pairs above (using cases (b) or (c), or case (a) with C3 after B2).
- B2 = 1 requires case (a), which excludes (2,1), leaving six pairs.

Total: 13 combinations.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 1 0
1 1 1
1 2 0
1 2 1
2 1 0
2 2 0
2 2 1
END