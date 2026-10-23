Q1, Q2 and Q3 are the values returned by A1, A2 and B2.

**Reading the sync points.** The "before P" line at the top of thread C has no steps above it, so it constrains nothing. B1 is before R. A2 ends after R, and so do A3 to A5. B4 and A5 both contain Q between their start and end.

**Writes.**
- y is written by C1 (1), C2 (2) and B3 (2).
- x is written by C3 (1) and A5 (1).

**History of y.** B1 returned 0, so no write to y happened before B1. C1 comes before C2, and B3 comes after B1 and B2. This leaves two possible histories of y:
- **H1:** 0, 1, 2, 2. This is B3 after C1.
- **H2:** 0, 2, 1, 2. This is B3 before C1, with C2 later giving the final 2.

A3, B4 and C4 all return 2, and both histories allow that.

**Pairs (A1, A2).** A1 comes before A2, so the pair is a non-decreasing pick from the history. A2's end is after R, but its effect instant is otherwise free.
- H1 gives (0,0), (0,1), (0,2), (1,1), (1,2), (2,2).
- H2 adds (2,1), because A1 can read the early 2 and A2 can then read 1.

**B2, the read of x.** B2 is before B3.
- B2 = 0 is always possible.
- B2 = 1 needs a write to x before B3. C3 can come after C2 and before B2, or A5 can come after A3 once a 2 exists. Both force C1 and C2 before B3, so the history is H1.
- Pair (2,1) needs H2, where B3 comes before C1. C3 comes after C2, so x is still 0 at B2. Hence (2,1) goes only with B2 = 0.

**Combinations.**

BEGIN
0 0 0
0 1 0
0 2 0
1 1 0
1 2 0
2 2 0
2 1 0
0 0 1
0 1 1
0 2 1
1 1 1
1 2 1
2 2 1
END