Only A1-A4 and B1-B5 matter here. B1, B2 and the reads of x don't affect the asked values, since x is never written and z is never read. With no sync points, the executions are all interleavings that keep each thread's order.

- **A2** reads y after A1 and before A3, so it sees 3, 1, or 2 (never 0, since A1 always precedes it).
- **B3** reads y before B4, so only A's writes can be visible: it returns 0 (before A1), 3 (after A1 with no A3 yet, or after A4), or 4 (after A3, before A4).
- **Final y** is the last write to y. A1 and B4 can never be last, because A3/A4 and B5 always come after them. So the final value is 3 (A4 last) or 2 (B5 last), and when B5 is last it comes after A4.

Checking each feasible placement of B3 and A2 against the possible orderings of B4, B5 and A4 gives these 12 combinations, in the order A2, B3, final y:

BEGIN
3 0 2
3 0 3
1 0 2
1 0 3
2 0 3
3 3 2
3 3 3
1 3 2
1 3 3
2 3 3
3 4 2
3 4 3
END