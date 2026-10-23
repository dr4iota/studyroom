**Approach.** There are no sync points, so any interleaving is allowed as long as each thread keeps its own order. Let v be the value B4 writes to y.

**The value of v.** B3 reads z after B2 writes 4 to z. The only other write to z is C1 (2).
- If C1 takes effect between B2 and B3, B3 returns 2.
- Otherwise B3 returns 4.

So v is 2 or 4. Every read of y then returns either 0 (before B4) or v (after B4).

**Limits on the reads of y.**
- A2 comes before A3. So if A3 returns 0, A2 also returns 0.
- If A3 returns v, A2 returns 0 or v.

**Which write to x is last.**
- **B1 (3):** B1 comes before B4.
  - If C3 returns v, C4 comes after B4, so after B1.
  - If A3 returns v, A4 comes after A3, which comes after B4, so after B1.
  - So 3 can be final only when A3 = 0 and C3 = 0. That case only needs C4 and A4 to finish before B1 starts, which is possible.
- **C2 (2):** C4 always follows C2 in thread C, so C2 is never last.
- **C4:** it writes the C3 result, which is 0 or v.
- **A4:** it writes the A2 result.
  - If A3 = 0, this is 0.
  - If A3 = v, it is 0 or v.

**Cases.**

| A3 | C3 | Final x |
|---|---|---|
| 0 | 0 | 0 (C4 or A4 last) or 3 (B1 last) |
| 0 | v | v (C4 last) or 0 (A4 last; A4 can be delayed until after C4) |
| v | 0 | 0 (C4 delayed until after A4) or v (A4 last, A2 = v) |
| v | v | v, or 0 (A4 last with A2 = 0) |

Every case with v appears for both v = 2 and v = 4. The constraint that C1 sits between B2 and B3 (giving v = 2) only rules out the final x = 3 path for v = 2. The combinations 0 0 0 and 0 0 3 do not involve v, so they still appear.

BEGIN
0 0 0
0 0 3
0 2 2
0 2 0
0 4 4
0 4 0
2 0 0
2 0 2
4 0 0
4 0 4
2 2 2
2 2 0
4 4 4
4 4 0
END