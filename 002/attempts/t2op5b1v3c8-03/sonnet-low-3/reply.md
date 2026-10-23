All combinations of (A5, B3) below are possible. A5 and B3 can only take the values 0, 1, 2 or 3.

**A5 = 3.** B can finish all its reads early and do its writes either before A4 or after A5. Then A5 reads A4's value, 3, and B3 can be any of 0, 1, 2, 3, depending on when it reads.

**A5 = v2, where v2 is the value B2 read and v2 ≠ 3.** B4 happens after B3, and B4 or B5 must take effect after A4 and before A5. So A5 reads B's rewrite of v2. B3 is read after B2, so it cannot see an earlier state of x than B2 saw.
- **v2 = 0:** B2 reads before A1. B3 can then read 0, 1, 2 or 3, so A5 = 0 pairs with every B3 value.
- **v2 = 2:** B2 reads between A1 and A2. B3 reads later, so it sees 2, 3 or 1 (never 0). A5 = 2 pairs with B3 = 1, 2, 3.
- **v2 = 1:** B2 reads between A3 and A4. B3 sees 1, or 3 if it reads after A4. A5 = 1 pairs with B3 = 1, 3.

If v2 = 3, then A5 = 3, which is already covered.

BEGIN
0 0
0 1
0 2
0 3
1 1
1 3
2 1
2 2
2 3
3 0
3 1
3 2
3 3
END