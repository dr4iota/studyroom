Every operation takes effect at a single instant, so each execution is an interleaving of A's and B's operations that keeps each thread's order. I split the cases by the value A1 reads. A4 writes that same value back to x, and it always comes after A3.

**Case A1 = 0 (A1 takes effect before B1).**
- A3 can take effect before B1, between B1 and B2, or after B2. So it returns 0, 1 or 3.
- B3 and B4 both come after B2, so they see either 3 (from B2) or 0 (from A4).
- If A4 takes effect before B2, B3 and B4 both see 3. If it takes effect after B4, they also both see 3. Result: (3, 3).
- If A4 takes effect between B2 and B3, both see 0. Result: (0, 0).
- If A4 takes effect between B3 and B4, B3 sees 3 and B4 sees 0. Result: (3, 0).
- When A3 = 3, A3 takes effect after B2 and A4 after A3. Placing A3 before B3 still allows all three placements of A4.
- Results: A3 ∈ {0, 1, 3}, each with (3, 3), (0, 0) or (3, 0).

**Case A1 = 1 (A1 takes effect between B1 and B2).**
- A3 returns 1 (before B2) or 3 (after B2).
- A4 writes 1. By the same placement argument, B3 and B4 can see (3, 3), (1, 1) or (3, 1).
- Results: A3 ∈ {1, 3}, each with those three pairs.

**Case A1 = 3 (A1 takes effect after B2).**
- A3 returns 3, since x holds 3 after B2.
- A4 writes 3 again, so B3 and B4 both return 3.
- Result: (3, 3, 3).

BEGIN
0 3 3
0 0 0
0 3 0
1 3 3
1 0 0
1 3 0
3 3 3
3 0 0
3 3 0
1 1 1
1 3 1
3 1 1
3 3 1
END