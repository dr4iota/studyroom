The reads A1–A4 all happen before A5, so they can only see B's writes. The other assumption I make is that **operations behave as if each took effect at one instant**, with all instants in one global order (sequential consistency).

**Values A2 and A4 can see.** Thread B's writes take effect in the order 1, 2, 3, 1. So x moves through the states:

| State index | 0 (initial) | 1 (after B2) | 2 (after B3) | 3 (after B4) | 4 (after B5) |
|---|---|---|---|---|---|
| Value of x | 0 | 1 | 2 | 3 | 1 |

- A2 sees the state at some index i, and A4 sees the state at some index j.
- A2 comes before A4, so i ≤ j.
- Listing every pair (value at i, value at j) gives these combinations:
  - i = 0: (0,0), (0,1), (0,2), (0,3)
  - i = 1: (1,1), (1,2), (1,3), (1,1)
  - i = 2: (2,2), (2,3), (2,1)
  - i = 3: (3,3), (3,1)
  - i = 4: (1,1)

**Value B1 can see.** B1 runs before B2, so B's own writes are not visible to it. The only other write is A5.

- **B1 = 1:** A5 must take effect before B1.
  - Then A1–A4 all take effect before B1, and therefore before B2.
  - So A2 = A4 = 0.
- **B1 = 0:** A5 takes effect after B1. This places no extra constraint, so every (A2, A4) pair above is possible.

BEGIN
0 0 0
0 1 0
0 2 0
0 3 0
1 1 0
1 2 0
1 3 0
2 1 0
2 2 0
2 3 0
3 1 0
3 3 0
0 0 1
END