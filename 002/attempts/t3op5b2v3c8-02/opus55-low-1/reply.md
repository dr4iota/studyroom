Every triple below is reachable, and every other triple is impossible. There are no sync points, so any interleaving that respects each thread's order is allowed. The argument works out which writes each read can see.

**Q1 (A1 reads x).** The writes to x are B2 (1), C1 (2) and A5 (2). A5 comes after A1 in thread A, so A1 can return:
- 0, if A1 takes effect before B2 and C1;
- 1, if B2 is the last write before A1;
- 2, if C1 is the last write before A1.

Call A1's result **a**. A3 later writes a to y.

**Q2 (B4 reads y).** B4 comes after B's own B3 (writes 1). B1 (writes 3) comes before B3, so B1 can never be the last write B4 sees. B4 can see:
- 1, from B3 or C3;
- 3, from A4 placed between B3 and B4;
- 2, from C2 placed between B3 and B4;
- a, from A3;
- whatever C4 returned, from C5.

**Q3 (C4 reads y).** C4 comes after C's own C3 (writes 1). C2 (writes 2) comes before C3, so C2 is never visible to C4. C4 can see:
- 1, from C3 or B3;
- 3, from A4, or from B1 placed after C3;
- a, from A3;
- whatever B4 returned, from B5.

**Cross-checks.**
- B4 cannot get its value from C5 while C4 gets its value from B5, because that would need each read to happen before the other. This removes nothing: whenever B4 and C4 return the same value, some other write can supply it.
- The constraints that fix A1's value only concern when A1 runs relative to B2 and C1. They do not conflict with placing A3, A4, B3 or C3 where the y reads need them.
- I checked an ordering for each mixed case. For example, to get B4 = a and C4 = 3: B3, A3, B4, C3, A4, C4.

**Resulting combinations.**
- **A1 = 0:** B4 is 0, 1, 2 or 3 and C4 is 0, 1 or 3. In addition, B4 = 2 with C4 = 2 works, because C4 can read the 2 written by B5.
- **A1 = 1:** B4 is 1, 2 or 3 and C4 is 1 or 3. In addition, B4 = 2 with C4 = 2 works.
- **A1 = 2:** B4 is 1, 2 or 3 and C4 is 1, 2 or 3. Here C4 = 2 is always possible, because A3 writes 2.

BEGIN
0 0 0
0 0 1
0 0 3
0 1 0
0 1 1
0 1 3
0 2 0
0 2 1
0 2 3
0 2 2
0 3 0
0 3 1
0 3 3
1 1 1
1 1 3
1 2 1
1 2 3
1 2 2
1 3 1
1 3 3
2 1 1
2 1 2
2 1 3
2 2 1
2 2 2
2 2 3
2 3 1
2 3 2
2 3 3
END