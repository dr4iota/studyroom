**Setup.** A3 writes 2 to x, yet A5 later reads 0. So some write of 0 to x must take effect after A3 and before A5. Only B4 and C5 can do that, and only if B2 or C3 returned 0. Neither has a sync point, so any order that respects each thread's sequence is allowed.

**Values of B2 and C3.** The only values ever in x are 0 and 2. Each of B2 and C3 returns either 0 or 2.
- If both returned 2, nobody writes 0 to x after A3. Then A5 cannot read 0, so (2, 2) is impossible.
- (0, 0), (0, 2) and (2, 0) are each possible, as shown by the orders below.

**Final value of z.** The writes to z are A4 (1), B1 (5), C1 (4) and C2 (1). C1 always comes before C2, so 4 can never be the final value. The final value is 1 or 5.

**Each combination (B2, C3, final z).**
- **(0, 0, 5):** C1, C2, C3(0), A1, A2, A3, C4, C5(x=0), A4, B1, B2(0), B3, B4(0), A5(0). B1 is the last write to z.
- **(0, 0, 1):** Use the same order but move B1 before A4. Then A4 is the last write to z.
- **(0, 2, 1):** B1, B2(0), A1, A2, A3, C1, C2, C3(2), C4, C5, B3, B4(0), A4, A5(0).
- **(0, 2, 5) is impossible.** C3 = 2 means C5 writes 2, so B2 cannot read a 0 written after A3. B2 must therefore come before A3. B1 comes before B2 and A3 comes before A4, so B1 is before A4 and cannot be the last write to z.
- **(2, 0, 5):** C1, C2, C3(0), A1, A2, A3, A4, B1, B2(2), B3, B4(2), C4, C5(0), A5(0).
- **(2, 0, 1):** Use the same order but move B1 before A4.

BEGIN
0 0 1
0 0 5
0 2 1
2 0 1
2 0 5
END