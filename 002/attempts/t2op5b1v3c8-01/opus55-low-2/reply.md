Every combination below is possible: 7 with B1 = 0 and B2 = 0, 10 with B2 = 1, 6 with B2 = 2 and 4 with B2 = 3. They come from tracking how far thread A has progressed when each of B's operations takes effect.

**Approach.** Thread A's writes take effect in the order 1, 1, 2, 3. So the value of x moves through 0 → 1 → 1 → 2 → 3. Let k be the number of A's writes that have taken effect, where k = 0 to 4. The value of x at each step is val(k) = 0, 1, 1, 2, 3.

Let k1 to k5 be A's progress when B1 to B5 take effect. These satisfy k1 ≤ k2 ≤ k3 ≤ k4 ≤ k5.

- **B1 and B2.** B1 returns val(k1) and B2 returns v2 = val(k2).
- **B3 and B4.** B3 writes v2.
  - If no A write falls between B3 and B4 (k4 = k3), B4 returns v2.
  - Otherwise B4 returns val(k4) for some k4 > k2.
- **Final value.** B5 writes v2.
  - If A has finished before B5 (k5 = 4), the final value is v2.
  - If A4 comes after B5, which needs k4 < 4, the final value is 3.
  - If B4 read 3 from A4, then A has already finished, so the final value must be v2.

**Cases by B2's value:**

- **v2 = 0 (k2 = 0, so B1 = 0).**
  - B4 can return 0, 1 or 2, each with final value 0 or 3.
  - B4 can also return 3, with final value 0.
- **v2 = 1 (k2 = 1 or 2, so B1 = 0 or 1).**
  - B4 can return 1 or 2, each with final value 1 or 3.
  - B4 can also return 3, with final value 1.
- **v2 = 2 (k2 = 3, so B1 = 0, 1 or 2).**
  - B4 can return 2, with final value 2 or 3.
  - B4 can also return 3, with final value 2.
- **v2 = 3 (k2 = 4, so B1 = 0, 1, 2 or 3).**
  - B4 returns 3 and the final value is 3.

BEGIN
0 0 0
0 0 3
0 1 0
0 1 3
0 2 0
0 2 3
0 3 0
0 1 1
0 2 1
0 3 1
1 1 1
1 1 3
1 2 1
1 2 3
1 3 1
0 2 2
0 3 2
1 2 2
1 3 2
2 2 2
2 2 3
2 3 2
0 3 3
1 3 3
2 3 3
3 3 3
END