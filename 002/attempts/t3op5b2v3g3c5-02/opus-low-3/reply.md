**Q1 (A1).** A1 can only return 0 or 2.
- The only writes to x are C1 (writes 2), A3 (writes A1's value) and B4 (writes B2's value).
- A3 comes after A1, so it cannot affect A1.
- B2 must read 0 or 2, so B4 also writes 0 or 2.

Both values can happen:
- **A1 = 2:** Run C1 before A1. A3 then writes 2, and B5 can read that 2.
- **A1 = 0:** A1 must run before C1. A3 cannot run before C1. If it did, A2 would also come before C1, and so before C2. Then A2 could not read 2. So the order must be A1 (reads 0), C1, B2 (reads 2), A3 (writes 0), B4 (writes 2), B5 (reads 2).

**Writes to y.** They are B1 (1), C2 (2), A4 (3) and C5 (C4's value). C4 runs after C2, so it reads 1, 2 or 3. C5 comes after C2, so C2 is never the last write. A2 reads 2, so the last write to y before A2 is C2 or a C5 that writes 2.

**Final y = 1.** This happens if B1 is last, or C5 is last after C4 read 1.
- B3 runs after B1. Only one later write of 2 could reach it, a C5 writing 2, and then y would not end at 1. So B3 cannot return 2.
- **B3 = 1:** for example, B1 is the last write and B3 reads it.
- **B3 = 3:** take this order: C2, A2, B1, C4 (reads 1), B2, A3, A4, B3 (reads 3), C5 (writes 1). This order works for A1 = 0 as well as A1 = 2.
- When A1 = 0, B1 cannot be the very last write. The x analysis forces A4 after B2, and B2 comes after B1. The order above still gives final y = 1 through C5.

**Final y = 2.** This needs C5 to be last, with C4 having read 2.
- **B3 = 1:** run B1, then B3, then C2.
- **B3 = 2:** B3 reads C2's value.
- **B3 = 3:** put A4 between C4 and C5, and B3 between A4 and C5.

**Final y = 3.** This needs A4 last, or C5 last after C4 read 3. B3 can read 1, 2 or 3 in suitable orders.

**Combining.** I built explicit orders for the cases above. I did not build a full order for every combination with A1 = 0. Those are included on the reasoning that the y orders above fit around the x order A1 = 0 requires.

BEGIN
0 1 1
0 3 1
0 1 2
0 2 2
0 3 2
0 1 3
0 2 3
0 3 3
2 1 1
2 3 1
2 1 2
2 2 2
2 3 2
2 1 3
2 2 3
2 3 3
END