Reasoning:

- **C3 returned 2.** The only write of 2 is A2, so A2 takes effect after C2 and before C3. B3 cannot fall between A2 and C3, so B3 is either before A2 or after C3.
- **A1** comes before A2. It can read 0 (before C1), 1 (between C1 and C2), or 3 (after C2, or after an early B3). So A1 can return 0, 1 or 3.
- **B3 before A2:** A2 is the last write, so x ends at 2. B1 comes before B3, which is before A2, so B1 can return 0, 1 or 3.
- **B3 after C3:** x ends at 3. B1 can return 0, 1, 3, or 2 (if it falls between A2 and B3).
- **The two reads don't constrain each other.** Every pairing of A1 and B1 values is reachable in each case. That gives 3×3 + 3×4 = 21 combinations.

BEGIN
0 0 2
0 1 2
0 3 2
1 0 2
1 1 2
1 3 2
3 0 2
3 1 2
3 3 2
0 0 3
0 1 3
0 2 3
0 3 3
1 0 3
1 1 3
1 2 3
1 3 3
3 0 3
3 1 3
3 2 3
3 3 3
END