Because A's writes are the only writes B can see in B1 and B2, those reads return values from A's sequence 0, 1, 2, 3, in non-decreasing order. Call the values v1 (B1) and v2 (B2), so v1 ≤ v2. B3 and B5 both write v2, which can overwrite a newer value of A and make x go backwards.

The final value is whichever write takes effect last. If A4 is last, x is 3. If B5 is last, x is v2.

**v2 = 0.** This forces v1 = 0. B3 writes 0, and A's writes can then land before B4, so v4 can be 0, 1, 2 or 3. The final value is 0 (B5 after A4) or 3 (A4 last). That gives 8 combinations.

**v2 = 1.** v1 can be 0 or 1. After B3 writes 1, x can never be 0 again, so v4 is 1, 2 or 3. The final value is 1 or 3. That gives 2 × 3 × 2 = 12 combinations.

**v2 = 2.** v1 can be 0, 1 or 2. After B3 writes 2, x is 2 or 3, so v4 is 2 or 3. The final value is 2 or 3. That gives 3 × 2 × 2 = 12 combinations.

**v2 = 3.** v1 can be 0, 1, 2 or 3. Then v4 = 3 and the final value is 3. That gives 4 combinations.

BEGIN
0 0 0
0 0 3
0 1 0
0 1 3
0 2 0
0 2 3
0 3 0
0 3 3
0 1 1
0 1 3
0 2 1
0 2 3
0 3 1
0 3 3
1 1 1
1 1 3
1 2 1
1 2 3
1 3 1
1 3 3
0 2 2
0 2 3
0 3 2
0 3 3
1 2 2
1 2 3
1 3 2
1 3 3
2 2 2
2 2 3
2 3 2
2 3 3
0 3 3
1 3 3
2 3 3
3 3 3
END