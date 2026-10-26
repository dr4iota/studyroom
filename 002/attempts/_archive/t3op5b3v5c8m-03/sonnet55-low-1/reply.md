Every combination of the three asked values is possible, so there are 12 in total.

**Which values can appear.** The only writes to x are A1 (writes 2) and B4 (writes whatever B2 read from y). Blocks y and z are written by B3, C3, C4 and A4 with values read from other blocks, plus C1 writing 3 to z. The value 3 can only ever end up in z, never in x or y. So B1 and the final x are each 0 or 2, and the final z is 0, 2 or 3.

**Q1 and Q2.** B1 can return 0 or 2, and the final x can be 0 or 2.

**Q3.** z ends as 3 when A4 runs before C1. Otherwise z ends as A3's value.

Each of the 12 combinations has a valid interleaving, built in the same way for all of them. B1 is set by whether B1 runs before or after A1. The final x is set by the order of A1 and B4, and by what B2 read from y. The final z is set by the order of A4 and C1, and by whether y was already 0 or 2 when A3 read it.

Examples:
- **B1=0, x=0, z=2:** B1, A1, B2 (reads 0), C2 (reads 2), C3 (y=2), A2, A3 (reads 2), C1, A4 (z=2), then B4 writes 0 to x.
- **B1=2, x=0, z=2:** A1, B1 (reads 2), B2 (reads 0), B3 (y=2), A2, A3 (reads 2), C1, A4 (z=2), then B4 writes 0 to x.
- **B1=2, x=2, z=2:** A1, C2 (reads 2), C3 (y=2), B1 (reads 2), B2 (reads 2), B4 (x=2), then A2, A3, C1 and A4 give z=2.
- **B1=0, x=2, z=any:** B1 reads 0 before A1, and A1 is the last write to x. For z=2, C2 reads 2 after A1 and C3 writes 2 to y before A3 reads it.

For z=0 or z=3 in each case, A3 reads y while it is still 0, and A4 runs after C1 (z=0) or before C1 (z=3).

BEGIN
0 0 0
0 0 2
0 0 3
0 2 0
0 2 2
0 2 3
2 0 0
2 0 2
2 0 3
2 2 0
2 2 2
2 2 3
END