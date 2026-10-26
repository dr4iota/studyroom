Since there are no sync points, any interleaving of the two threads is allowed.

**Notation.** Let *k* be the number of A's writes that have taken effect so far. The value of x from A's writes alone is 0, 1, 1, 2, 3 for k = 0, 1, 2, 3, 4. Let k1, k2, k3, k4 and k5 be the values of k when B1, B2, B3, B4 and B5 take effect. These satisfy k1 ≤ k2 ≤ k3 ≤ k4 ≤ k5. Let a be the value read by B1 and b the value read by B2.

**What B4 and the final value can be.**
- If no A write falls between B3 and B4 (k4 = k3), B4 reads b, because B3 wrote b.
- Otherwise B4 reads A's value at k4. That stage is after k2, so it is a later value than b.
- If B5 takes effect after A4 (k5 = 4), the final value is b.
- Otherwise A4 is the last write and the final value is 3.
- If k4 = 4, then k5 = 4, so the final value must be b.

**Case b = 0 (k2 = 0, so a = 0).**
- B4 = 0: the final value is 0 or 3.
- B4 = 1 or 2 (k4 < 4): the final value is 0 or 3.
- B4 = 3 (k4 = 4): the final value is 0.

**Case b = 1 (k2 = 1 or 2, so a = 0 or 1).**
- B4 = 1 or 2: the final value is 1 or 3.
- B4 = 3: the final value is 1.

**Case b = 2 (k2 = 3, so a = 0, 1 or 2).**
- B4 = 2: the final value is 2 or 3.
- B4 = 3: the final value is 2.

**Case b = 3 (k2 = 4, so a = 0, 1, 2 or 3).**
- B4 = 3 and the final value is 3.

The answers below are ordered as B1, B4, then the final value of x.

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