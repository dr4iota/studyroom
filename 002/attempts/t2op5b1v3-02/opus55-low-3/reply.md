I modeled this as one shared block x, where every operation takes effect at a single instant (rule 2).

**Approach.** Thread B's writes take effect in the order 3, 2, 1, 2. Let k be the number of B writes that have taken effect before a given A operation. The value of x at each stage is:

| k | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| v(k) | 0 | 3 | 2 | 1 | 2 |

Thread A's operations take effect in program order. So their stages satisfy k2 ≤ k3 ≤ k4 ≤ k5, with A2 at stage k2, A3 at k3, A4 at k4 and A5 at k5. This gives:

- A2 returns v(k2), and A3 returns v(k3).
- A5 returns A4's own value 2 if no B write takes effect between A4 and A5 (k5 = k4).
- Otherwise A5 returns v(k5), which can be any v(k) with k > k3.
- So A5 can return 2, or v(k) for any k > k3.

**Cases by k3**

- **k3 = 0:** A2 = 0 and A3 = 0. A5 can be 2, 3 or 1.
- **k3 = 1:** A3 = 3, and A2 is 0 or 3. A5 can be 2 or 1.
- **k3 = 2:** A3 = 2, and A2 is 0, 3 or 2. A5 can be 2 or 1.
- **k3 = 3:** A3 = 1, and A2 is 0, 3, 2 or 1. A5 can only be 2.
- **k3 = 4:** A3 = 2, and A2 is 0, 3, 2 or 1. A5 can only be 2.

**Check on one edge case.** A2 = 1, A3 = 2 is only possible with k3 = 4. B has then finished all its writes, so A5 must return 2. "1 2 1" is therefore impossible.

BEGIN
0 0 2
0 0 3
0 0 1
0 3 2
0 3 1
3 3 2
3 3 1
0 2 2
0 2 1
3 2 2
3 2 1
2 2 2
2 2 1
0 1 2
3 1 2
2 1 2
1 1 2
1 2 2
END