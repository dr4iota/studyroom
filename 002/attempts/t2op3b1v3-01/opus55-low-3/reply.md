Every combination of A2 and A3 occurs with B1 = 0 and with B1 = 1, giving 12 outcomes.

**Approach.** Each operation takes effect at one instant, so every run is an interleaving of A1→A2→A3 with B1→B2→B3. A read returns the last write to x before it.

**B1.** B1 takes effect before B2, so only A1 can have written x before it.
- If B1 comes before A1, it returns 0.
- If B1 comes after A1, it returns 1.

**A2 and A3.** Both reads come after A1. Each returns whichever write was last before it: A1 (1), B2 (3) or B3 (2). B2 always takes effect before B3, and A3 comes after A2. So A3's last write is the same as A2's or later in the order of writes.

**Case B1 = 1 (A1 before B1, so A1 before B2 and B3).** The write order is 1, 3, 2. The (A2, A3) pairs follow that order without going backwards: (1,1), (1,3), (1,2), (3,3), (3,2), (2,2).

**Case B1 = 0 (B1 before A1).** A1 can still take effect before B2, which again gives all six pairs above. Placing A1 between B2 and B3, or after B3, only produces pairs already in that list. So B1 = 0 also allows all six.

BEGIN
1 1 0
1 3 0
1 2 0
3 3 0
3 2 0
2 2 0
1 1 1
1 3 1
1 2 1
3 3 1
3 2 1
2 2 1
END