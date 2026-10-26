Each outcome is listed as (B1, B3, final x).

**Values x can hold.** Thread A's writes happen in program order. Ignoring B4, x goes through the values 0 → 3 (A1) → 1 (A2) → A3's value (A4) → 2 (A5).

- If B4 does not take effect between A2 and A3, A3 reads 1, so A4 writes 1 again.
- If B4 does take effect between A2 and A3, A3 reads B4's value and A4 writes that value again. This is covered under Case 2.

B1, B2, B3 and B4 take effect in that order. B4 writes the value B2 read.

**Case 1: B4 takes effect after A5.**
- The final value of x is whatever B2 read.
- B1, B2 and B3 all happen before B4, so they only see values written by A.
- Those values appear in the order 0, 3, 1, 2. The reads can only move forward through that order, so B1 ≤ B2 ≤ B3 in position.

Listing every such choice of (B1, B3, B2):
- B1 = 0:
  - B2 = 0: (0,0,0), (0,3,0), (0,1,0), (0,2,0)
  - B2 = 3: (0,3,3), (0,1,3), (0,2,3)
  - B2 = 1: (0,1,1), (0,2,1)
  - B2 = 2: (0,2,2)
- B1 = 3: (3,3,3), (3,1,3), (3,2,3), (3,1,1), (3,2,1), (3,2,2)
- B1 = 1: (1,1,1), (1,2,1), (1,2,2)
- B1 = 2: (2,2,2)

**Case 2: B4 takes effect before A5.**
- A5 writes last, so the final value of x is 2.
- B3 happens before B4, and B4 happens before A5. So B3 reads one of 0, 3 or 1, never B4's value and never 2.
- B1 reads at the same point as B3 or earlier in the order 0, 3, 1.

This gives (0,0,2), (0,3,2), (0,1,2), (3,3,2), (3,1,2), (1,1,2).

Combining both cases:

BEGIN
0 0 0
0 3 0
0 1 0
0 2 0
0 3 3
0 1 3
0 2 3
0 1 1
0 2 1
0 2 2
3 3 3
3 1 3
3 2 3
3 1 1
3 2 1
3 2 2
1 1 1
1 2 1
1 2 2
2 2 2
0 0 2
0 3 2
0 1 2
3 3 2
3 1 2
1 1 2
END