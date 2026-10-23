Reasoning:

- B1 and B2 finish before P. B3 and B4 come after B2 but are not tied to P.
- A2 ends after P, so A3 and A4 happen after B2 has taken effect. A3 therefore can never read 0.
- A2 starts early and may take effect before B2, so it can read 0. Otherwise it reads whichever of 3, 2, 1 is current, and the writes to x land in the order 3, 2, 1.
- A3 happens after A2's effect, so it reads a value no earlier in that order than A2's.
- A4 rewrites A3's value at some point after A3, which sets the final value of x:
  - A3 = 3: A4 either lands after B4, leaving 3, or before B4, leaving 1.
  - A3 = 2: A4 either lands after B4, leaving 2, or before B4, leaving 1.
  - A3 = 1: the final value is 1.

BEGIN
0 3 3
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END