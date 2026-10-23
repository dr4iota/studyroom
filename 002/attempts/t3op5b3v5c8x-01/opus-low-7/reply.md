Here are the possible outcomes as (B5, C4, final y). There are no sync points, so any interleaving of the three threads is allowed. Let **a** be the value A1 reads from z; A2 and A3 write a back to z, and A4 writes a to y.

**Where each value can come from**
- z can hold 1 (from B1 or from A when a=1), 2 (from C1 or from A when a=2), or 0.
- B5 and C4 run after B1 and C1 respectively. So either can return 0 only if a=0 and one of A's writes lands after B1 or C1.
- B3 writes b, the value B2 read from x. b=1 if C2 comes before B2, and b=0 otherwise.
- Final y is a or b, whichever of A4 and B3 takes effect last.
- **y=2 needs a=2 and A4 after B3.** If a=2, neither read can return 0. So y=2 is possible only for (1,1), (1,2), (2,1) and (2,2), and each has a valid order.

**Case a=0** (A1 runs before B1 and C1), so y ∈ {0,1}
- **(2,1) is impossible here.** C4=1 forces C1 < B1 < C4 with no write between B1 and C4. B5=2 forces B1 < C1 < B5 with no write between C1 and B5. Both orders cannot hold.
- **(2,0) allows only y=0.** B5=2 and C4=0 force C1 < B5 < (A's write) < C4. So A4 comes after B3, and y = a = 0.
- **Every other pair allows both y=0 and y=1.** For y=1, put C2 before B2 and B3 after A4. For y=0, put A4 last, or let B2 read 0. Example for (0,0,1): A1, C1, C2, B1, B2(reads 1), A2, A3, A4, B3, B4, B5(reads 0), C3, C4(reads 0).

**Pair (2,1) when a≠0**
- **a=1:** B5=2 needs B5 before the 1-write that C4 reads, and that write must be A's. So A4 comes after B3, giving only y=1.
- **a=2:** the order is C1 < A1 < B1 < C4 < A2 < B5.
  - A4 after B3 gives y=2.
  - A4 before B3 gives y=b, which can be 1 or 0. Example for y=1: C1, A1, B1, C2, B2, C3, C4, A2, A3, A4, B3, B4, B5. Moving B2 before C2 gives y=0.

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
2 1 0
2 1 1
2 1 2
2 2 0
2 2 1
2 2 2
END