Both threads' ordinary steps happen before P, except the operations that straddle it.

**What each read can return**
- **B1 (read x):** B1 can return 0, 3, or 1, depending on whether it falls before A1, between A1 and A3, or after A3. Call this value v.
- **B2 (read y):** B2 comes after B1 and before B3 starts, so B3's write cannot affect it. It returns 0 if it comes before A2, otherwise 2.
- **Final y:** B4 runs after B3 ends and after P. A's last write to y (A2) is long finished by then. So the final y is always v.
- **A4 (read y):** A4 starts after A3 and ends after P, so it can take effect before B3's write, between B3 and B4, or after B4. It returns 2, 3, or v respectively.

**Combinations by v**
- **v = 0:** B1 is before A1, so B2 can be 0 or 2. A4 can be 2, 3, or 0. The final y is 0.
- **v = 3:** B1 is between A1 and A3, so B2 can be 0 or 2. A4 can be 2 or 3. The final y is 3.
- **v = 1:** B1 is after A3, and A2 is before A3, so B2 must be 2. A4 can be 2, 3, or 1. The final y is 1.

BEGIN
2 0 0
2 2 0
3 0 0
3 2 0
0 0 0
0 2 0
2 0 3
2 2 3
3 0 3
3 2 3
2 2 1
3 2 1
1 2 1
END