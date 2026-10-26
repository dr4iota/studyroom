Every possible combination of (A7, A8, B8) is 2 1 6, 2 0 6 or 2 0 1.

**1. All of thread B happens before A2.** B8 must end before Q, and B runs its steps in order, so B1–B8 all finish before Q. A2 must start after Q. So all of B is done before A2 starts. The only thread-A operation that can overlap with B is A1 (write 1 to y), which has no sync constraint.

**2. Thread B's reads.**
- B1 and B2 read x. The only writes to x are B5 and A5, and both come later. So B1 and B2 return 0.
- B3 reads y. It returns 1 if A1 took effect before it, otherwise 0.
- B5 writes B3's value to x.
- B6 writes 0 (B2's value) to y, then B7 writes 6 to y.
- B8 reads y. It returns 1 if A1 takes effect between B7 and B8, otherwise 6.

**3. Where A1 can fall:**

| A1 takes effect | B3 returns | x after B5 | B8 returns |
|---|---|---|---|
| before B3 | 1 | 1 | 6 |
| between B3 and B6 | 0 | 0 | 6 |
| between B6 and B7 | 0 | 0 | 6 |
| between B7 and B8 | 0 | 0 | 1 |
| after B8 | 0 | 0 | 6 |

**4. Thread A after Q.**
- A2 reads x and gets B3's value; call it v.
- A3 writes 2 to z.
- A4 writes v to y, and A5 writes v to x.
- No later write to z exists, so A7 reads 2.
- No later write to y exists, so A8 reads v.

**5. Results.**
- If v = 1, B8 returns 6, giving 2 1 6.
- If v = 0, B8 returns 6 or 1, giving 2 0 6 and 2 0 1.

The remaining sync points (P, R, S) can be placed to fit all of these orderings.

BEGIN
2 1 6
2 0 6
2 0 1
END