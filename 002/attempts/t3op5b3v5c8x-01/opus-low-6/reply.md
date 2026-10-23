Every combination of B5, C4 and final y is possible except the five where y is 2 and B5 or C4 returns 0. That leaves 22 outcomes.

**Setup.** No thread has a sync point, so any interleaving that keeps each thread's own order is allowed.

- Let a be the value A1 reads from z, so a ∈ {0, 1, 2}. A2, A3 and A4 then write a to z, z and y.
- Let b be the value B2 reads from x, so b ∈ {0, 1}. B3 writes b to y.
- The final y is whichever of A4 and B3 takes effect last, so y ∈ {a, b}.
- The writes to z are B1 (1), C1 (2), A2 (a) and A3 (a). B5 comes after B1, and C4 comes after C1.

**When y = 2.** This needs a = 2. Then every write to z is 1 or 2, so neither B5 nor C4 can return 0. All four combinations of 1 and 2 work. For example, take the order C1, A1, B1, C2, C3, C4(→1), A2, A3, B2, B3, A4, B4, B5(→2). This gives (2, 1, 2).

**When B5 or C4 returns 0.** This needs a = 0, so A1 must take effect before both B1 and C1. A2 and A3 can then write 0 at any point afterwards.

- y = 0 always works, since a = 0.
- y = 1 needs B2 to follow C2 (so b = 1) and B3 to follow A4.
- In both cases B5 and C4 can be given any values from {0, 1, 2} by placing the writes suitably. The one exception is (B5, C4) = (2, 1), which I check next.

**The pair (B5 = 2, C4 = 1).**

- If a = 0, this is impossible. C4 would need B1 to follow C1, and B5 would need C1 to follow B1.
- It works with a = 2. The order C1, A1, C2, C3, B1, C4(→1), A2, A3, A4, B2, B3, B4, B5(→2) gives y = 1.
- The order C1, A1, B1, B2(→0), A4, B3, C2, C3, C4(→1), A2, B4, B5(→2) gives y = 0.

**Impossible outcomes.** The only outcomes that cannot happen are y = 2 together with a 0 for B5 or C4: (0,0,2), (0,1,2), (0,2,2), (1,0,2) and (2,0,2).

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 0 0
1 0 1
1 1 0
1 1 1
1 1 2
1 2 0
1 2 1
1 2 2
2 0 0
2 0 1
2 1 0
2 1 1
2 1 2
2 2 0
2 2 1
2 2 2
END