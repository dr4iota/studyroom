All 27 combinations of (A1, A2, A3) are possible, with each value drawn from {0, 2, 3}.

**Which values can appear**
- y can hold 0, 3 (from B2, or copied by C4) or 2 (from B3, or copied by C4). So A1 can return 0, 2 or 3.
- x can hold 0, 3 (from B1 or a copy) or 2 (from B5 when B4 read 2). C2 can also write 0 back into x if C1 read 0 before B1. So A2 and A3 can each return 0, 2 or 3.

**Why every combination works**
- A1 = 0: A1 runs before any write to y. All later writes then happen after A2 and A3 can be placed freely, so any x sequence is available.
- A1 = 3: A1 runs between B2 and B3, or after C4 has copied a 3.
- A1 = 2: A1 runs after B3. Any x value is still reachable afterwards, because C2 can reset x to 0 and C4 can later put a 3 into y for B5 to copy.

The orderings that look hardest are all achievable:
- x going 3 → 0: B1 writes 3, then C2 writes 0, having read 0 before B1.
- x going 2 → 0: B5 writes 2, then C2 writes 0, having read 0 before B1.
- x going 2 → 3: B1 writes 3, C1 reads 3, B5 writes 2, then C2 writes 3.
- x going 0 → 3 or 0 → 2: A2 reads the initial 0, then B1 or B5 writes later.

Equal pairs (0 0, 2 2, 3 3) occur when no write to x lands between A2 and A3.

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 2
0 3 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
2 3 0
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 2 0
3 2 2
3 2 3
3 3 0
3 3 2
3 3 3
END