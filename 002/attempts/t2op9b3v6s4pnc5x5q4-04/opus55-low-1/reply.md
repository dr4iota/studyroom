**Ordering constraints from the sync points**
- B1 and B2 come before Q, and Q comes before A9.
- A9 comes before R, and R comes before B8.
- A3 onward comes after P, and P comes after B1.
- A1 comes before S, and S comes before B5.

**A4 (read z).**
- The writes to z are A1 (6), B1 (1), A6, A9 and B8.
- A6 and A9 are A's own later steps, and B8 comes after R, so it is after A4.
- A1 is before A4 because it is in A's own order. B1 is before A4 because B1 < P < A3.
- B1 and A1 can occur in either order. So A4 returns 6 if A1 took effect after B1, and 1 if A1 took effect before B1. Call this value v (1 or 6).

**A7 and y.**
- A6 writes v to z. No other write to z can fall between A6 and A7, so A7 reads v.
- A8 writes v to y. A8 is the only write to y, so the final y is v.

**B2 (read y).** It returns 0 if it takes effect before A8, or v if after. Both are allowed.

**z and B9.**
- A9 writes v to z, but B8 comes after R, which is after A9.
- So B8's write (B2's value) is the last write to z.
- B9 reads that value, and the final z equals it too.

**Final x.**
- B7 (write 4) is normally the last write to x.
- A2 (write 1) is only bounded by A2 > A1 and A2 < A9 < R. So A2 can take effect after B7, which is after S, and then the final x is 1.
- If B2 returned v, then A2 < A8 < B2 < B7, so the final x must be 4.
- If B2 returned 0, the final x can be 1 or 4.

**Possible combinations**
| B2 | Final x | B9 / final z |
|---|---|---|
| 0 | 1 or 4 | 0 |
| v | 4 | v |

Each row holds for v = 1 and for v = 6, giving six combinations.

BEGIN
0 1 1 0
0 4 1 0
1 4 1 1
0 1 6 0
0 4 6 0
6 4 6 6
END